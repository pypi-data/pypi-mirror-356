import logging
import os
import pprint
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import concurrent.futures

from flask import Request, jsonify
import google.oauth2.service_account
from google.apps import chat_v1 as google_chat
from google.protobuf import field_mask_pb2

# --- Logging Setup ---
# Configure logging based on environment variable or default to DEBUG
log_level_name = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
log_level = getattr(logging, log_level_name, logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
# Silence excessively verbose loggers from dependencies if needed
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('watchdog').setLevel(logging.INFO) # Silence specific loggers

# Main logger for this module
logger = logging.getLogger(__name__)


# --- Base Agent Class ---
class GChatBotFlask(ABC):
    """
    Abstract base class for building Google Chat bots using Flask.

    Handles incoming HTTP requests from Google Chat, parses event payloads,
    extracts key information (user, space, message, command), and routes
    events to appropriate processing methods.

    This implementation uses a hybrid approach:
    1. First attempts to process the request synchronously with a timeout.
    2. If processing completes quickly, returns a direct response.
    3. If processing exceeds the timeout, switches to asynchronous mode:
       a. Responding immediately with 200 OK
       b. Starting a background thread to process the request
       c. Posting a "Processing..." message and updating it when done

    Subclasses MUST implement the abstract methods `_process_slash_command`
    and `_process_message` to define the bot's specific logic.
    """

    # Default OAuth scopes required for the service account to post/update messages
    DEFAULT_APP_AUTH_SCOPES = ["https://www.googleapis.com/auth/chat.bot"]
    
    # Default timeout for synchronous processing before switching to async mode
    DEFAULT_SYNC_TIMEOUT = 5.0  # seconds

    def __init__(self,
                 bot_name: str = "GoogleChatBot",
                 bot_image_url: Optional[str] = None, # Optional image URL
                 service_account_file: Optional[str] = None,
                 app_auth_scopes: Optional[list[str]] = None,
                 sync_timeout: float = DEFAULT_SYNC_TIMEOUT):
        """
        Initializes the Google Chat Bot agent.

        Args:
            bot_name: The display name of the bot, used for mentions and card headers.
            bot_image_url: Optional URL for the bot's avatar image in cards.
                           Defaults to a generic icon if not provided.
            service_account_file: Path to the Google Service Account JSON key file.
                                  Required for asynchronous message posting/updating.
            app_auth_scopes: List of OAuth scopes for the service account.
                             Defaults to DEFAULT_APP_AUTH_SCOPES.
            sync_timeout: Maximum time in seconds to wait for synchronous processing
                         before switching to asynchronous mode.
        """
        self.bot_name = bot_name
        # Use a default image if none provided
        self.bot_image_url = bot_image_url or "https://developers.google.com/chat/images/quickstart-app-avatar.png"
        self.service_account_file = service_account_file
        self.app_auth_scopes = app_auth_scopes or self.DEFAULT_APP_AUTH_SCOPES
        self.sync_timeout = sync_timeout
        self.logger = logging.getLogger(self.__class__.__name__) # Logger specific to the subclass

        # Load service account credentials immediately if path is provided
        self._app_credentials = None
        if self.service_account_file:
            self._app_credentials = self._load_app_credentials()
        else:
             self.logger.warning(
                 "Service account file not provided. Asynchronous features "
                 "(posting/updating messages) will be disabled."
             )

        self.logger.info(f"{self.__class__.__name__} initialized (Name: {self.bot_name}).")

    # --- Service Account Credential Handling ---

    def _load_app_credentials(self) -> Optional[google.oauth2.service_account.Credentials]:
        """
        Loads Google Service Account credentials from the specified file path.

        Returns:
            The loaded Credentials object, or None if loading fails.
        """
        if not self.service_account_file:
            # This should ideally not be reached if called internally after check in __init__
            self.logger.error("Cannot load app credentials: service_account_file path is not set.")
            return None
        try:
            creds = google.oauth2.service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=self.app_auth_scopes)
            self.logger.info(f"Service account credentials loaded successfully from {self.service_account_file}.")
            return creds
        except FileNotFoundError:
            self.logger.error(f"Service account file not found: {self.service_account_file}")
            return None
        except Exception as e:
            self.logger.exception(f"Failed to load service account credentials from {self.service_account_file}: {e}")
            return None

    def _get_app_credentials_client(self) -> Optional[google_chat.ChatServiceClient]:
         """
         Creates a google.apps.chat_v1.ChatServiceClient instance authenticated
         using the loaded service account credentials.

         Returns:
             An authenticated ChatServiceClient instance, or None if credentials
             could not be loaded or the client could not be created.
         """
         # Attempt to load credentials if not already loaded (e.g., if path was provided after init)
         if not self._app_credentials:
             self.logger.warning("App credentials not loaded previously. Attempting to load now.")
             self._app_credentials = self._load_app_credentials()
             if not self._app_credentials:
                 self.logger.error("Failed to get app client: Credentials could not be loaded.")
                 return None

         # Create the client using the loaded credentials
         try:
             client = google_chat.ChatServiceClient(credentials=self._app_credentials)
             self.logger.debug("ChatServiceClient with app credentials created successfully.")
             return client
         except Exception as e:
             self.logger.exception(f"Failed to create ChatServiceClient with app credentials: {e}")
             return None

    # --- Synchronous Processing with Timeout ---
    
    def _timed_processing(self, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Execute the core event processing logic with a time limit.
        
        This is called by handle_request to attempt synchronous processing
        before potentially switching to asynchronous mode.
        
        Args:
            extracted_data: The extracted data from the event.
            event_data: The original event data.
            
        Returns:
            The response text from processing the event.
        """
        return self._process_event(extracted_data, event_data)

    # --- Format Response for Synchronous Returns ---
    
    def _format_response(self, response_text: str, event_data: Dict[str, Any]) -> Any:
        """
        Formats the response into the JSON structure expected by Google Chat API
        for synchronous replies.

        Args:
            response_text: The text content to be displayed in the card.
            event_data: The original event payload from Google Chat.

        Returns:
            A Flask JSON response object with the properly formatted payload.
        """
        # Extract user display name for the card header
        # This logic handles different event structures
        user_info = event_data.get('user')
        if 'chat' in event_data:
             # For Chat App API events, user might be nested differently
             user_info = event_data.get('chat', {}).get('user', user_info)
        user_display_name = user_info.get('displayName', 'Usuário') if user_info else 'Usuário'

        # Use the unified card creation method
        response_card = self._create_response_card(response_text, user_display_name)
        
        # Build payload based on event type
        if 'chat' in event_data:
            # Format for Chat App API events
            response_payload = {
                "hostAppDataAction": {
                    "chatDataAction": {
                        "createMessageAction": {
                            "message": {
                                "cardsV2": [response_card]
                            }
                        }
                    }
                }
            }
        else:
            # Format for direct messages/webhooks
            response_payload = {"cardsV2": [response_card]}
        
        self.logger.debug(f"Sending response payload:\n {pprint.pformat(response_payload)}")
        return jsonify(response_payload)

    # --- Card Creation --- 

    def _create_response_card(self, card_text: str, user_display_name: str) -> Dict[str, Any]:
        """
        Creates the standard card structure used for bot responses.
        Used for both synchronous replies and asynchronous updates to maintain consistency.

        Args:
            card_text: The main text content for the card's body.
            user_display_name: The display name of the user the response is directed to.

        Returns:
            A dictionary representing the JSON structure for a Google Chat card.
        """
        return {
            "card": {
                "header": {
                    "title": self.bot_name,
                    "subtitle": f"Para: {user_display_name}",
                    "image_url": self.bot_image_url,
                    "image_type": "CIRCLE",
                    "image_alt_text": self.bot_name
                },
                "sections": [{
                    "widgets": [{
                        "text_paragraph": {
                            "text": card_text
                        }
                    }]
                }]
            }
        }

    # --- Asynchronous Processing Logic ---

    def _handle_async_response(self, future: concurrent.futures.Future, extracted_data: Dict[str, Any]):
        """
        Waits for an already-running task (Future) to complete, then handles
        posting and updating the Google Chat message. This runs in a background
        thread and, crucially, does NOT re-run the business logic.

        Args:
            future: The Future object representing the original, in-progress task.
            extracted_data: Data parsed by _extract_event_data, used for creating the response.
        """
        app_client = self._get_app_credentials_client()
        space_name = extracted_data.get("space_name")
        user_display = extracted_data.get("user_display_name", "Usuário")

        if not app_client or not space_name or space_name == 'Unknown Space':
            self.logger.error(f"Cannot handle async response for space '{space_name}': App client or space name is unavailable.")
            # We can't report an error back to the user, so we just log and exit.
            return

        processing_message_name = None
        try:
            # 1. Send an initial "Processing..." message to the user.
            self.logger.debug(f"Sending 'Processing...' card message to space: {space_name}")
            processing_card_text = "🔄 Processando sua solicitação..."
            initial_card = self._create_response_card(processing_card_text, user_display)
            processing_message_req = google_chat.CreateMessageRequest(
                parent=space_name,
                message=google_chat.Message(cards_v2=[initial_card])
            )
            sent_message = app_client.create_message(request=processing_message_req)
            processing_message_name = sent_message.name
            self.logger.info(f"Sent 'Processing...' message ({processing_message_name}) to space {space_name}")

            # 2. Wait for the original future to complete and get its result.
            # This is the key change: we are NOT running _process_event again.
            self.logger.debug(f"Waiting for original future to complete for message {processing_message_name}...")
            final_response_text = future.result()  # This blocks until the original task is done.
            self.logger.debug(f"Original future completed for {processing_message_name}. Result received.")

            # 3. Update the "Processing..." message with the final result.
            self.logger.debug(f"Attempting to update message {processing_message_name} with final result.")
            final_card = self._create_response_card(final_response_text, user_display)
            update_message_req = google_chat.UpdateMessageRequest(
                message=google_chat.Message(
                    name=processing_message_name,
                    cards_v2=[final_card]
                ),
                update_mask="cardsV2"
            )
            app_client.update_message(request=update_message_req)
            self.logger.info(f"Successfully updated message {processing_message_name} with final card response.")

        except Exception as e:
            # This will catch exceptions from this method OR exceptions raised by the original `future`.
            self.logger.exception(f"Error during async response handling for space {space_name} (Initial msg: {processing_message_name}): {e}")

            # If we managed to post the "Processing..." message, try to update it with an error.
            if processing_message_name and app_client:
                try:
                    self.logger.warning(f"Attempting to update message {processing_message_name} with error details.")
                    error_text = f"❌ Ocorreu um erro ao processar sua solicitação: {type(e).__name__}"
                    error_card = self._create_response_card(error_text, user_display)
                    error_update_req = google_chat.UpdateMessageRequest(
                        message=google_chat.Message(
                            name=processing_message_name,
                            cards_v2=[error_card]
                        ),
                        update_mask="cardsV2"
                    )
                    app_client.update_message(request=error_update_req)
                    self.logger.info(f"Successfully updated message {processing_message_name} with error card details.")
                except Exception as update_err:
                    self.logger.exception(f"Failed to update message {processing_message_name} with error card details: {update_err}")

    # --- Request Handling ---

    def handle_request(self, request: Request) -> Any:
        """
        Main entry point for handling HTTP requests from Google Chat via Flask.

        This implements the hybrid approach:
        1. Attempts to process the request synchronously with a timeout
        2. If processing completes within timeout, returns direct response
        3. If timeout is exceeded, switches to asynchronous mode:
           - Returns immediate 200 OK
           - Starts background thread
           - Posts "Processing..." message and updates when done

        Args:
            request: The Flask request object containing the Google Chat event payload.

        Returns:
            Either:
            - A formatted response if processing completes within timeout
            - An empty response (jsonify({})) if switching to async mode
            - An error response if request validation fails
        """
        # Handle simple GET requests (e.g., for health checks or simple info)
        if request.method == 'GET':
            self.logger.debug("Received GET request.")
            return jsonify({"status": "active", "message": f"{self.bot_name} está ativo. Use POST para eventos."}), 200

        # Ensure the request is POST
        if request.method != 'POST':
            self.logger.warning(f"Received unsupported HTTP method: {request.method}")
            return jsonify({"error": "Method not allowed"}), 405

        # Process POST request (Google Chat event)
        try:
            event_data = request.get_json(silent=True)
            if not event_data:
                # Google Chat sometimes sends empty POSTs for verification, ignore them silently.
                self.logger.debug("Received empty or invalid JSON payload. Returning empty 200 OK.")
                return jsonify({}) # Return 200 OK as required by Chat API for some events
            
            # Log the raw event data only if debug level is enabled
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"Received event data:\n{pprint.pformat(event_data)}")

            # Extract key information (user, space, message, command, etc.)
            extracted_data = self._extract_event_data(event_data)
            if not extracted_data:
                # If extraction fails, log the issue and return OK
                self.logger.warning("Could not extract necessary data from the event. Returning empty 200 OK.")
                return jsonify({})

            # Check if service account credentials are available
            # If not, we can only do synchronous processing
            if not self._app_credentials:
                self.logger.warning("No service account credentials available. Processing synchronously only.")
                response_text = self._process_event(extracted_data, event_data)
                return self._format_response(response_text, event_data)

            # Try to process with timeout using concurrent.futures
            # This is more reliable than the threading approach for timeouts
            self.logger.debug(f"Attempting synchronous processing with {self.sync_timeout}s timeout")
            result = None
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            future = executor.submit(self._timed_processing, extracted_data, event_data)
            try:
                # Wait for the result with a timeout
                result = future.result(timeout=self.sync_timeout)
                self.logger.info("Processing completed within timeout. Responding synchronously.")
                # Return formatted response directly
                executor.shutdown(wait=False)
                return self._format_response(result, event_data)
            except concurrent.futures.TimeoutError:
                # Timeout occurred. Switch to robust asynchronous mode.
                self.logger.info(f"Processing exceeded timeout of {self.sync_timeout}s. Switching to robust asynchronous mode.")
                
                # The future is still running. We start a "monitor" thread to wait for it
                # and handle the response when it's done.
                # We pass the *original future* to the new thread, not re-running the task.
                thread = threading.Thread(
                    target=self._handle_async_response,
                    args=(future, extracted_data.copy())
                )
                thread.daemon = True
                thread.start()
                
                # Tell the executor to clean up its resources after the running future is done.
                # `wait=False` allows us to return the 200 OK immediately.
                self.logger.debug("Returning immediate 200 OK to Google Chat (async mode).")
                executor.shutdown(wait=False)
                return jsonify({})

        except Exception as e:
            # --- Final Exception Handling for Request Processing --- 
            # This catches any unexpected errors during the initial request handling 
            # (parsing, credential checks, sync attempt) before a standard response 
            # (sync or async OK) could be sent. Errors within the async thread 
            # are handled separately inside _handle_async_response.
            self.logger.exception(f"Critical error handling incoming request: {e}")
            # Return a generic error message *in the immediate response* if possible
            error_response = {"text": "Ocorreu um erro interno ao processar a solicitação."}
            return jsonify(error_response), 500 # Internal Server Error


    # --- Event Payload Parsing Logic ---
    # These methods parse different structures Google Chat might send.

    def _parse_app_command_payload(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parses events triggered via the slash command UI (`appCommandPayload`).

        Structure: `event_data['chat']['appCommandPayload']`
        User: `message['sender']` (preferred) or `event_data['user']`
        Space: `message['space']` or `payload['space']`
        """
        try:
            chat_data = event_data.get('chat', {})
            payload = chat_data.get('appCommandPayload', {})
            if not payload: return None

            message = payload.get('message', {})
            user = message.get('sender') # Prioritize sender from message
            if not user:
                self.logger.debug("Sender not in message (appCommandPayload), falling back to event_data['user'].")
                user = event_data.get('user')

            space = message.get('space', payload.get('space')) # Space can be in message or payload

            if not user or not space:
                 self.logger.warning("User or Space data missing in 'appCommandPayload' structure.")
                 return None

            return {
                "message": message,
                "user": user,
                "space": space,
                "is_direct_message_event": False # Slash commands are not DMs
            }
        except Exception as e:
            self.logger.exception(f"Error parsing app command payload: {e}")
            return None

    def _parse_message_payload(self, chat_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parses an alternative event structure within the 'chat' key (`messagePayload`).
        May be used by specific Chat App API interactions.

        Structure: `event_data['chat']['messagePayload']`
        User: `chat_data['user']`
        Space: `message['space']`
        """
        try:
            payload = chat_data.get('messagePayload', {})
            if not payload: return None

            user = chat_data.get('user')
            message = payload.get('message', {})
            space = message.get('space')

            if not user or not message or not space:
                 self.logger.warning("User, Message or Space data missing in 'messagePayload' structure.")
                 return None

            return {
                "message": message,
                "user": user,
                "space": space,
                "is_direct_message_event": False # Assume not DM for this structure
            }
        except Exception as e:
            self.logger.exception(f"Error parsing message payload: {e}")
            return None

    def _parse_direct_message_event(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parses standard direct messages or messages in spaces (webhook/API style).

        Structure: Top-level `message`, `user`, `space` keys.
        User: `event_data['user']`
        Space: `event_data['space']`
        """
        try:
            message = event_data.get('message')
            user = event_data.get('user')
            space = event_data.get('space')

            if not message or not user or not space:
                 self.logger.warning("Message, User or Space data missing in direct message/webhook structure.")
                 return None

            is_direct_message_event = space.get('type') == 'DM'
            return {
                "message": message,
                "user": user,
                "space": space,
                "is_direct_message_event": is_direct_message_event
            }
        except Exception as e:
            self.logger.exception(f"Error parsing direct message/webhook payload: {e}")
            return None

    def _parse_unstructured_chat_event(self, chat_data: Dict[str, Any], event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Fallback parser when 'chat' key exists but lacks known payload structures.
        Attempts to find top-level 'message', 'user', 'space'.
        """
        self.logger.debug(f"Unrecognized structure within 'chat' key: {list(chat_data.keys())}. Attempting fallback parsing.")
        try:
            user = event_data.get('user')
            # Check for message at top level first (might be ADDED_TO_SPACE event inside 'chat')
            message = event_data.get('message', {})
            # Prefer space from message if available, else top-level space
            space = message.get('space', event_data.get('space'))

            if not message or not user: # Require at least user and some message structure
                self.logger.warning("Could not find sufficient user or message data in unstructured 'chat' event.")
                return None

            return {
                "message": message,
                "user": user,
                "space": space or {}, # Ensure space is a dict even if None initially
                "is_direct_message_event": False # Assume not DM if structure is unknown
            }
        except Exception as e:
             self.logger.exception(f"Error parsing unstructured chat event: {e}")
             return None

    def _parse_fallback_event(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Minimal parser for unrecognized top-level structures (e.g., ADDED_TO_SPACE).
        Tries to find user info in 'commonEventObject' or top-level 'user'.
        """
        self.logger.debug(f"Unrecognized top-level event structure: {list(event_data.keys())}. Attempting minimal fallback parsing.")
        try:
            # Look for user info in common structure or top-level as last resort
            common_event = event_data.get('commonEventObject', {})
            user = common_event.get('user', event_data.get('user'))

            if not user: # If no user info found anywhere, cannot proceed meaningfully
                self.logger.error("Failed to identify user from event data in fallback.")
                return None

            # Cannot reliably determine message or space in this unknown structure.
            self.logger.warning("Could not reliably determine message or space from fallback structure.")
            return {
                "message": {}, # Empty message
                "user": user,
                "space": {},   # Empty space
                "is_direct_message_event": False,
                "is_fallback": True # Flag indicating minimal parsing occurred
            }
        except Exception as e:
            self.logger.exception(f"Error parsing fallback event: {e}")
            return None

    # --- Command and Argument Parsing ---

    def _parse_command_and_arguments(self, message: Dict[str, Any], bot_name: str) -> Optional[Dict[str, Optional[str]]]:
        """
        Extracts command, arguments, and processed text from a message object.

        Handles slash commands (via annotations or manual typing) and bot mentions.

        Args:
            message: The message dictionary from the parsed event payload.
            bot_name: The configured name of this bot instance.

        Returns:
            A dictionary containing:
            {
                'command': str | None, # The command name without '/' or None
                'arguments': str,      # Arguments string following the command
                'processed_text': str, # Text relevant for processing (args for commands, text after mention for messages)
                'raw_text': str        # The original, unmodified message text
            }
            or None if parsing fails unexpectedly.
        """
        try:
            # raw_text: Original text content from the message, stripped.
            raw_text = message.get('text', '').strip()
            # argumentText: Text provided after a slash command (from UI) or often after a leading mention.
            argument_text_ui = message.get('argumentText', '').strip()
            # text_to_process: Starts as raw_text, but can be overwritten if a leading mention is detected via annotations.
            text_to_process = raw_text
            # Annotations: Structured data from the API about mentions, slash commands, etc.
            annotations = message.get('annotations', [])

            command = None
            arguments = ""
            # processed_text: The text relevant for command arguments or message processing, 
            # potentially derived from argumentText or text_to_process after modification.
            processed_text = ""

            # --- 1. Check for Leading Bot Mention via Annotations (Most Reliable Method) --- 
            # This is preferred over string manipulation (startswith) because it uses structured API data.
            leading_bot_mention = False
            for annotation in annotations:
                # Check if there's a user mention annotation...
                if (
                    annotation.get('type') == 'USER_MENTION' and
                    # ...that starts exactly at the beginning of the raw text...
                    annotation.get('startIndex') == 0 and
                    # ...and mentions a bot.
                    annotation.get('userMention', {}).get('user', {}).get('type') == 'BOT' 
                ):
                    # If a leading bot mention is confirmed via annotation,
                    # trust 'argumentText' as the source for the actual command/text that follows.
                    text_to_process = argument_text_ui # Use the stripped argumentText
                    leading_bot_mention = True
                    self.logger.debug(f"Leading Bot mention found via annotation. Using argumentText for subsequent processing: '{text_to_process}'")
                    break # Found the leading mention, no need to check other annotations for this purpose.
            
            # --- [Fallback] Handle Bot Mentions via startswith (If not found via annotation) ---
            # This is less reliable due to potential formatting issues but kept as a fallback.
            if not leading_bot_mention:
                mention_trigger = f"@{bot_name}"
                if text_to_process.startswith(mention_trigger): 
                    text_to_process = text_to_process[len(mention_trigger):].strip()
                    self.logger.debug(f"[Fallback] Bot mention detected via startswith. Processing text after mention: '{text_to_process}'")
            
            # --- 2. Check for Slash Command (Invoked via Chat UI - Annotation Preferred) ---
            # Checks if the interaction was triggered by clicking a registered slash command suggestion.
            slash_command_annotation = None
            for annotation in annotations:
                if annotation.get('type') == 'SLASH_COMMAND' and 'slashCommand' in annotation:
                    slash_command_annotation = annotation['slashCommand']
                    self.logger.debug(f"Slash command found via UI annotation: {slash_command_annotation}")
                    break

            if slash_command_annotation:
                # If triggered via UI, extract command name from the annotation.
                command = slash_command_annotation.get('commandName', '').strip('/')
                # Arguments specifically come from 'argumentText' when using UI-triggered commands.
                arguments = argument_text_ui 
                processed_text = arguments # For commands, the relevant text are the arguments.
                self.logger.debug(f"Parsed command from UI Annotation: command='{command}', arguments='{arguments}'")

            # --- 3. Check for Manually Typed Slash Command ---
            # This runs only if a command wasn't identified via UI annotation.
            # It checks the text_to_process (which might have been updated by mention handling).
            elif text_to_process.strip().startswith('/'): 
                # Strip again right before checking to be safe.
                text_to_process_stripped = text_to_process.strip()
                self.logger.debug(f"Potential manually typed slash command found (starts with '/'). Text being parsed: '{text_to_process_stripped}'")
                # Parse the command and arguments from the text.
                parts = text_to_process_stripped[1:].split(" ", 1) 
                command = parts[0].lower()
                arguments = parts[1].strip() if len(parts) > 1 else ''
                processed_text = arguments # Arguments are the relevant text for commands.
                self.logger.debug(f"Parsed command from Manual Text: command='{command}', arguments='{arguments}'")

            # --- 4. Handle as Regular Message ---
            # If no slash command (UI or manual) was detected.
            else:
                # The remaining text in 'text_to_process' is treated as a simple message.
                # This text is either the original message or the text after a leading mention was removed.
                self.logger.debug(f"Parsing as regular message (no command identified). Processed text: '{text_to_process}'")
                processed_text = text_to_process 
                arguments = processed_text # For simple messages, arguments can be considered the whole text.

            # Return the parsed components.
            return {
                "command": command,
                "arguments": arguments,
                "processed_text": processed_text,
                "raw_text": raw_text,
            }
        except Exception as e:
             self.logger.exception(f"Error parsing command and arguments: {e}")
             return None

    # --- Event Data Orchestration ---

    def _extract_event_data(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Orchestrates the parsing of various Google Chat event payload structures.

        Identifies the payload type and delegates to specific `_parse_*` methods.
        Combines basic info (user, space, message) with command/argument details.

        Args:
            event_data: The raw JSON payload dictionary from the Google Chat event.

        Returns:
            A dictionary containing consolidated, extracted data:
            {
                "raw_text": str,
                "processed_text": str,
                "command": str | None,
                "arguments": str,
                "user_email": str,
                "user_display_name": str,
                "space_name": str, # Format: "spaces/XXXXXXXXXXX" or "Unknown Space"
                "is_direct_message_event": bool,
                "message_name": str | None, # Format: "spaces/XXX/messages/YYY" or None
                "is_fallback_event": bool # True if only minimal parsing was possible
            }
            or None if essential data (like user) cannot be parsed.
        """
        parsed_basics = None
        try:
            # --- 1. Identify payload structure and perform basic parsing ---
            # Attempt different parsing strategies based on expected payload structures.
            # The first successful parser determines the basic info (message, user, space).
            # Determine which parser to use based on top-level keys
            if 'chat' in event_data:
                chat_data = event_data['chat']
                if 'appCommandPayload' in chat_data:
                    self.logger.debug("Parsing structure: App Command Payload")
                    parsed_basics = self._parse_app_command_payload(event_data)
                elif 'messagePayload' in chat_data:
                    self.logger.debug("Parsing structure: Message Payload")
                    parsed_basics = self._parse_message_payload(chat_data)
                else:
                    # 'chat' key exists, but no known sub-payload structure
                    self.logger.debug("Parsing structure: Unstructured Chat Event")
                    parsed_basics = self._parse_unstructured_chat_event(chat_data, event_data)
            elif 'message' in event_data:
                 # Standard structure for direct messages or webhook-style events
                self.logger.debug("Parsing structure: Direct Message/Webhook Event")
                parsed_basics = self._parse_direct_message_event(event_data)
            else:
                # Handles unknown structures, ADDED_TO_SPACE, REMOVED_FROM_SPACE etc.
                self.logger.debug("Parsing structure: Fallback Event")
                parsed_basics = self._parse_fallback_event(event_data)

            # --- 2. Validate basic parsing results ---
            # Need at least user info. Message/Space might be empty dicts in fallback cases.
            if not parsed_basics or not parsed_basics.get('user'):
                self.logger.warning("Failed to parse basic event structure (user missing or parsing failed). Cannot extract data.")
                return None

            # Extract results from the successful parser
            message = parsed_basics.get('message', {}) # Will be {} in successful fallback
            user = parsed_basics['user']
            space = parsed_basics.get('space', {}) # Will be {} in successful fallback
            is_direct_message_event = parsed_basics.get('is_direct_message_event', False)
            is_fallback_event = parsed_basics.get('is_fallback', False)

            # --- 3. Extract common user/space details ---
            user_email = user.get('email', 'Unknown Email')
            user_display_name = user.get('displayName', 'Unknown User')
            # Ensure space_name is handled gracefully if space is missing/empty
            space_name = space.get('name') if space else None
            if not space_name: # Handle cases where space might be {} or None
                 space_name = 'Unknown Space'
                 if not is_fallback_event: # Only warn if not expected fallback
                      self.logger.warning("Could not determine space name from parsed data.")

            # --- 4. Parse command, arguments, and text details ---
            # Requires a message structure, skip if it was a minimal fallback parse
            command_data = None
            if not is_fallback_event and message: # Ensure message is not empty
                command_data = self._parse_command_and_arguments(message, self.bot_name)
                if command_data is None: # Check if the command parser itself failed
                    self.logger.error("Failed to parse command and arguments from message content.")
                    # Decide if we should return None or proceed with partial data.
                    # Returning None for safety as command/args are usually key.
                    return None
            else:
                # Minimal data for fallback events (no command/text parsing possible/reliable)
                 if is_fallback_event:
                     self.logger.debug("Fallback event type detected: Skipping command/argument parsing.")
                 else: # Should not happen if message is required earlier, but as safety
                     self.logger.warning("Message data missing or empty: Skipping command/argument parsing.")
                 # Provide default empty values
                 command_data = {
                     "command": None, "arguments": "", "processed_text": "", "raw_text": ""
                 }

            # --- 5. Combine all extracted data into final dictionary ---
            extracted = {
                "raw_text": command_data["raw_text"],
                "processed_text": command_data["processed_text"],
                "command": command_data["command"],
                "arguments": command_data["arguments"],
                "user_email": user_email,
                "user_display_name": user_display_name,
                "space_name": space_name,
                "is_direct_message_event": is_direct_message_event,
                "message_name": message.get("name"), # Original message ID (e.g., spaces/XXX/messages/YYY) or None
                "is_fallback_event": is_fallback_event
            }
            if self.logger.isEnabledFor(logging.INFO): # Log final only if INFO enabled
                 # Ensure the f-string is properly formed on a single logical line
                 self.logger.info(f"Event data extracted successfully:\n{pprint.pformat(extracted)}")
            return extracted

        except Exception as e:
            # Catch-all for unexpected errors during the extraction orchestration
            self.logger.exception(f"Critical error during event data extraction: {e}")
            return None


    # --- Event Processing Router ---

    def _process_event(self, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Routes the event to the appropriate handler (_process_slash_command or
        _process_message) based on the extracted data.

        This method is called by the asynchronous processing thread.

        Args:
            extracted_data: The dictionary of data extracted by `_extract_event_data`.
            event_data: The original raw event payload (passed for context if needed by handlers).

        Returns:
            The response text string generated by the specific handler.
            This string will be used to update the "Processing..." message.
        """
        command = extracted_data.get("command")
        arguments = extracted_data.get("arguments", "") # Default to empty string
        processed_text = extracted_data.get("processed_text", "") # Default to empty string

        # Route based on whether a command was identified
        if command:
            self.logger.info(f"Routing to slash command handler: /{command}")
            # Call the abstract method implemented by the subclass
            return str(self._process_slash_command(command, arguments, extracted_data, event_data))
        else:
            self.logger.info("Routing to message handler.")
            # Call the abstract method implemented by the subclass
            return str(self._process_message(processed_text, extracted_data, event_data))


    # --- Abstract Methods (To be implemented by subclasses) ---

    @abstractmethod
    def _process_slash_command(self, command: str, arguments: str, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Abstract method to handle recognized slash commands.
        Subclasses MUST implement this method to define command logic.

        Args:
            command: The name of the slash command (e.g., 'help') without '/'.
            arguments: The arguments string provided after the command name.
            extracted_data: The dictionary of data extracted from the event.
            event_data: The original raw event payload.

        Returns:
            The text response to be displayed in the chat.
        """
        # Example implementation in subclass:
        # if command == 'help':
        #     return "This is the help text."
        # else:
        #     return f"Unknown command: /{command}"
        raise NotImplementedError("Subclasses must implement _process_slash_command")

    @abstractmethod
    def _process_message(self, text: str, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Abstract method to handle regular messages (direct messages or mentions
        where no slash command was detected).
        Subclasses MUST implement this method to define message response logic.

        Args:
            text: The processed text of the message (e.g., mention removed).
            extracted_data: The dictionary of data extracted from the event.
            event_data: The original raw event payload.

        Returns:
            The text response to be displayed in the chat.
        """
        # Example implementation in subclass:
        # if "hello" in text.lower():
        #     return f"Hello {extracted_data['user_display_name']}!"
        # else:
        #     return "I received your message."
        raise NotImplementedError("Subclasses must implement _process_message")

    # Note: _format_response method was removed as responses are now sent/updated
    # asynchronously using the Chat API client, not returned directly via HTTP.
    # Card formatting, if needed, should happen within the _process_* methods
    # or within _handle_async_response before updating the message (though the
    # current implementation only updates text).