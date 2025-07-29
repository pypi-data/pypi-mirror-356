import asyncio
import json
import logging
import os
import pprint
import threading
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Union, Tuple, Callable, Awaitable

import google.oauth2.service_account
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from google.apps import chat_v1 as google_chat
from google.protobuf import field_mask_pb2

from .types import (
    AppCommandPayload,
    ChatData,
    ChatMessage,
    ChatMessageAnnotation,
    ChatSpace,
    ChatUser,
    CommonEventObject,
    EventPayload,
    ExtractedEventData,
    ParsedBasics,
    ParsedCommand,
    ProgressiveResponse,
    ResponseType,
)
from .response import ResponseFactory
from .parser import EventParser
from .processor import AsyncProcessor

# Get the top-level logger for this library
# This is done once when the module is imported.
logger = logging.getLogger('gchatbot')

# --- Base Agent Class ---
class GChatBot(ABC):
    """
    Abstract base class for building Google Chat bots using FastAPI.

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

    Subclasses MUST implement the abstract methods `_processSlashCommand`
    and `_processMessage` to define the bot's specific logic.
    """

    # Default OAuth scopes required for the service account to post/update messages
    DEFAULT_APP_AUTH_SCOPES = ["https://www.googleapis.com/auth/chat.bot"]

    # Default timeout for synchronous processing before switching to async mode
    DEFAULT_SYNC_TIMEOUT = 5.0  # seconds

    def __init__(self,
                 botName: str = "GoogleChatBot",
                 botImageUrl: Optional[str] = None, # Optional image URL
                 serviceAccountFile: Optional[str] = None,
                 appAuthScopes: Optional[list[str]] = None,
                 syncTimeout: float = DEFAULT_SYNC_TIMEOUT,
                 debug: bool = False,
                 processingMessage: str = "🔄 Processando sua solicitação..."):
        """
        Initializes the Google Chat Bot agent.

        Args:
            botName: The display name of the bot, used for mentions and card headers.
            botImageUrl: Optional URL for the bot's avatar image in cards.
                           Defaults to a generic icon if not provided.
            serviceAccountFile: Path to the Google Service Account JSON key file.
                                  Required for asynchronous message posting/updating.
            appAuthScopes: List of OAuth scopes for the service account.
                             Defaults to DEFAULT_APP_AUTH_SCOPES.
            syncTimeout: Maximum time in seconds to wait for synchronous processing
                         before switching to asynchronous mode.
            debug: If True, sets the library's log level to DEBUG. Defaults to False.
            processingMessage: The message to display while processing.
        """
        self.botName = botName
        # Use a default image if none provided
        self.botImageUrl = botImageUrl or "https://developers.google.com/chat/images/quickstart-app-avatar.png"
        self.serviceAccountFile = serviceAccountFile
        self.appAuthScopes = appAuthScopes or self.DEFAULT_APP_AUTH_SCOPES
        self.syncTimeout = syncTimeout
        self.logger = logging.getLogger(__name__) # Logger specific to this module (e.g., gchatbot.main)
        self.processingMessage = processingMessage

        # Configure library logging level based on the debug flag
        logLevel = logging.DEBUG if debug else logging.INFO
        logger.setLevel(logLevel)

        # If the library's logger has no handlers, add a NullHandler
        # to prevent "No handler found" warnings. The user's application
        # is responsible for configuring the actual handlers (e.g., StreamHandler).
        if not logger.hasHandlers():
            logger.addHandler(logging.NullHandler())

        # Instantiate modular components
        self.responseFactory = ResponseFactory(self.botName, self.botImageUrl)
        self.eventParser = EventParser(self.botName)
        self.asyncProcessor = AsyncProcessor(
            getAppCredentialsClient=self._getAppCredentialsClient,
            responseFactory=self.responseFactory,
        )

        # Load service account credentials immediately if path is provided
        self._appCredentials = None
        if self.serviceAccountFile:
            self._appCredentials = self._loadAppCredentials()
        else:
             self.logger.warning(
                 "Service account file not provided. Asynchronous features "
                 "(posting/updating messages) will be disabled."
             )

        self.logger.info(f"{self.__class__.__name__} initialized (Name: {self.botName}).")

    # --- Service Account Credential Handling ---

    def _loadAppCredentials(self) -> Optional[google.oauth2.service_account.Credentials]:
        """
        Loads Google Service Account credentials from the specified file path.

        Returns:
            The loaded Credentials object, or None if loading fails.
        """
        if not self.serviceAccountFile:
            # This should ideally not be reached if called internally after check in __init__
            self.logger.error("Cannot load app credentials: serviceAccountFile path is not set.")
            return None
        try:
            creds = google.oauth2.service_account.Credentials.from_service_account_file(
                self.serviceAccountFile, scopes=self.appAuthScopes)
            self.logger.info(f"Service account credentials loaded successfully from {self.serviceAccountFile}.")
            return creds
        except FileNotFoundError:
            self.logger.error(f"Service account file not found: {self.serviceAccountFile}")
            return None
        except Exception as e:
            self.logger.exception(f"Failed to load service account credentials from {self.serviceAccountFile}: {e}")
            return None

    def _getAppCredentialsClient(self) -> Optional[google_chat.ChatServiceClient]:
         """
         Creates a google.apps.chat_v1.ChatServiceClient instance authenticated
         using the loaded service account credentials.

         Returns:
             An authenticated ChatServiceClient instance, or None if credentials
             could not be loaded or the client could not be created.
         """
         # Attempt to load credentials if not already loaded (e.g., if path was provided after init)
         if not self._appCredentials:
             self.logger.warning("App credentials not loaded previously. Attempting to load now.")
             self._appCredentials = self._loadAppCredentials()
             if not self._appCredentials:
                 self.logger.error("Failed to get app client: Credentials could not be loaded.")
                 return None

         # Create the client using the loaded credentials
         try:
             client = google_chat.ChatServiceClient(credentials=self._appCredentials)
             self.logger.debug("ChatServiceClient with app credentials created successfully.")
             return client
         except Exception as e:
             self.logger.exception(f"Failed to create ChatServiceClient with app credentials: {e}")
             return None

    # --- Synchronous Processing with Timeout ---

    def _timedProcessing(self, extractedData: ExtractedEventData, eventData: EventPayload) -> str:
        """
        Execute the core event processing logic.
        This is a synchronous method designed to be run in a separate thread
        to avoid blocking the asyncio event loop.

        Args:
            extractedData: The consolidated, structured data from the event.
            eventData: The original, raw event payload from Google Chat.

        Returns:
            The response text string generated by the bot's processing logic.
        """
        return self._processEvent(extractedData, eventData)

    # --- Request Handling ---

    async def handleRequest(self, request: Request) -> Any:
        """
        Main entry point for handling HTTP requests from Google Chat via FastAPI.

        This method implements the hybrid synchronous/asynchronous processing model.
        1. It first attempts to process the request and generate a response within
           a defined timeout (`self.syncTimeout`).
        2. If processing completes within the timeout, it returns a direct JSON response.
        3. If the timeout is exceeded, it switches to asynchronous mode:
           - Returns an immediate empty 200 OK response to the Google Chat API.
           - Starts a background thread to continue processing the request.
           - In the thread, it posts a "Processing..." message and later updates it
             with the final result.

        Args:
            request: The incoming FastAPI request object containing the Google Chat event payload.

        Returns:
            A `fastapi.responses.JSONResponse` containing the message payload if
            processing is synchronous and successful. An empty `JSONResponse` if
            switching to asynchronous mode.

        Raises:
            HTTPException: If the request method is not supported or an internal
                           error occurs during initial request handling.
        """
        # Handle simple GET requests (e.g., for health checks or simple info)
        if request.method == 'GET':
            self.logger.debug("Received GET request.")
            return JSONResponse(content={"status": "active", "message": f"{self.botName} está ativo. Use POST para eventos."})

        # Ensure the request is POST
        if request.method != 'POST':
            self.logger.warning(f"Received unsupported HTTP method: {request.method}")
            raise HTTPException(status_code=405, detail="Method Not Allowed")

        # Process POST request (Google Chat event)
        try:
            eventData = None
            try:
                # Read body first to check if it's empty. Google Chat sometimes sends empty POSTs.
                body = await request.body()
                if not body:
                    self.logger.debug("Received empty payload. Returning empty 200 OK.")
                    return JSONResponse(content={}) # Return 200 OK as required
                eventData = json.loads(body)
            except json.JSONDecodeError:
                self.logger.warning("Received invalid JSON payload. Returning empty 200 OK.")
                return JSONResponse(content={})

            # Log the raw event data only if debug level is enabled
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"Received event data:\n{pprint.pformat(eventData)}")

            # Extract key information (user, space, message, command, etc.)
            extractedData = self.eventParser.extractEventData(eventData)
            if not extractedData:
                # If extraction fails, log the issue and return OK
                self.logger.warning("Could not extract necessary data from the event. Returning empty 200 OK.")
                return JSONResponse(content={})

            # Check if service account credentials are available
            # If not, we can only do synchronous processing
            if not self._appCredentials:
                self.logger.warning("No service account credentials available. Processing synchronously only.")
                # Check if we need async processing
                hasAsyncMethods = (
                    inspect.iscoroutinefunction(self._processMessage) or 
                    inspect.iscoroutinefunction(self._processSlashCommand)
                )
                
                if hasAsyncMethods:
                    responseText = await self._processEventAsync(extractedData, eventData)
                else:
                    responseText = self._processEvent(extractedData, eventData)
                responsePayload = self.responseFactory.formatSyncResponse(responseText, eventData)
                return JSONResponse(content=responsePayload)

            # Detect if we need async processing
            hasAsyncMethods = (
                inspect.iscoroutinefunction(self._processMessage) or 
                inspect.iscoroutinefunction(self._processSlashCommand)
            )

            if hasAsyncMethods:
                # Use async processing
                processing_task = asyncio.create_task(
                    self._processEventAsync(extractedData, eventData)
                )
            else:
                # Use sync processing in thread
                processing_task = asyncio.create_task(
                    asyncio.to_thread(self._processEvent, extractedData, eventData)
                )

            try:
                # Wait for the task to complete, but only for a short time.
                result = await asyncio.wait_for(processing_task, timeout=self.syncTimeout)

                # If it completes in time, respond synchronously.
                self.logger.info("Processing completed within timeout. Responding synchronously.")
                responsePayload = self.responseFactory.formatSyncResponse(result, eventData)
                return JSONResponse(content=responsePayload)

            except asyncio.TimeoutError:
                # If it times out, the task is still running in the background.
                # We launch a "monitor" task that will handle the async response
                # when the original task is done. We do NOT re-run the logic.
                self.logger.info(f"Processing exceeded timeout of {self.syncTimeout}s. Switching to robust asynchronous mode.")

                # The 'processing_task' future is passed to the async handler.
                asyncio.create_task(
                    self.asyncProcessor.handleAsyncResponse(processing_task, extractedData)
                )

                # Return immediate 200 OK to Google Chat API.
                self.logger.debug("Returning immediate 200 OK to Google Chat (async mode).")
                return JSONResponse(content={})

        except Exception as e:
            # --- Final Exception Handling for Request Processing ---
            # This catches any unexpected errors during the initial request handling
            # (parsing, credential checks, sync attempt) before a standard response
            # (sync or async OK) could be sent. Errors within the async thread
            # are handled separately inside _run_async_processing.
            self.logger.exception(f"Critical error handling incoming request: {e}")
            # Return a generic error message
            raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar a solicitação.")


    # --- Event Processing Router ---

    def _processEvent(self, extractedData: ExtractedEventData, eventData: EventPayload) -> str:
        """
        Routes the event to the appropriate handler based on the extracted data.

        This method supports both sync and async processing methods by detecting
        if the user's methods are async and handling them appropriately.

        Args:
            extractedData: The dictionary of consolidated data from `_extractEventData`.
            eventData: The original event payload, passed for context if a handler needs it.

        Returns:
            The response text string generated by the specific handler. This string
            will be used to create the final response card.
        """
        command = extractedData.get("command")
        arguments = extractedData.get("arguments", "") # Default to empty string
        processedText = extractedData.get("processedText", "") # Default to empty string

        # Route based on whether a command was identified
        if command:
            self.logger.info(f"Routing to slash command handler: /{command}")
            # Check if _processSlashCommand is async
            if inspect.iscoroutinefunction(self._processSlashCommand):
                # For async methods, we need to handle them in an async context
                # Since this method is called from asyncio.to_thread, we need to
                # create a new event loop for the async operation
                self.logger.warning("Async _processSlashCommand detected. This requires async processing context.")
                return "❌ Método async detectado. Use processamento assíncrono completo."
            else:
                # Call the synchronous method
                result = self._processSlashCommand(command, arguments, extractedData, eventData)
                
                # Check if it's a progressive response
                if self._isProgressiveResponse(result):
                    quickResponse, _ = result
                    self.logger.info("Progressive response detected in sync context - returning quick response only")
                    return str(quickResponse)
                
                return str(result) if result is not None else "Comando processado."
        else:
            self.logger.info("Routing to message handler.")
            # Check if _processMessage is async
            if inspect.iscoroutinefunction(self._processMessage):
                # For async methods, we need to handle them in an async context
                self.logger.warning("Async _processMessage detected. This requires async processing context.")
                return "❌ Método async detectado. Use processamento assíncrono completo."
            else:
                # Call the synchronous method
                result = self._processMessage(processedText, extractedData, eventData)
                
                # Check if it's a progressive response
                if self._isProgressiveResponse(result):
                    quickResponse, _ = result
                    self.logger.info("Progressive response detected in sync context - returning quick response only")
                    return str(quickResponse)
                
                return str(result) if result is not None else "Mensagem processada."


    async def _processEventAsync(self, extractedData: ExtractedEventData, eventData: EventPayload) -> str:
        """
        Async version of _processEvent that can properly handle async processing methods.

        Args:
            extractedData: The dictionary of consolidated data from `_extractEventData`.
            eventData: The original event payload, passed for context if a handler needs it.

        Returns:
            The response text string generated by the specific handler.
        """
        command = extractedData.get("command")
        arguments = extractedData.get("arguments", "") # Default to empty string
        processedText = extractedData.get("processedText", "") # Default to empty string

        # Route based on whether a command was identified
        if command:
            self.logger.info(f"Routing to async slash command handler: /{command}")
            # Check if _processSlashCommand is async
            if inspect.iscoroutinefunction(self._processSlashCommand):
                result = await self._processSlashCommand(command, arguments, extractedData, eventData)
            else:
                result = self._processSlashCommand(command, arguments, extractedData, eventData)
            
            # Check if it's a progressive response
            if self._isProgressiveResponse(result):
                return await self._handleProgressiveResponse(tuple(result), extractedData)
            
            return str(result) if result is not None else "Comando processado."
        else:
            self.logger.info("Routing to async message handler.")
            # Check if _processMessage is async
            if inspect.iscoroutinefunction(self._processMessage):
                result = await self._processMessage(processedText, extractedData, eventData)
            else:
                result = self._processMessage(processedText, extractedData, eventData)
            
            # Check if it's a progressive response
            if self._isProgressiveResponse(result):
                return await self._handleProgressiveResponse(tuple(result), extractedData)
            
            return str(result) if result is not None else "Mensagem processada."


    # --- Abstract Methods (To be implemented by subclasses) ---

    @abstractmethod
    def _processSlashCommand(self, command: str, arguments: str, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        Abstract method to handle recognized slash commands.
        Subclasses MUST implement this method to define their command logic.
        Can be implemented as either sync or async method.

        Args:
            command: The name of the slash command (e.g., 'help'), without the '/'.
            arguments: The arguments string provided after the command name.
            extractedData: The consolidated, structured data from the event.
            eventData: The original event payload, for context if needed.

        Returns:
            str: Simple response text
            OR
            Tuple[str, Union[str, Callable, Coroutine]]: Progressive response
            - First element: Quick response (immediate)
            - Second element: Detailed response (processed later)
        """
        pass

    @abstractmethod
    def _processMessage(self, text: str, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        Abstract method to handle regular messages (DMs or mentions without a command).
        Subclasses MUST implement this method to define their message processing logic.
        Can be implemented as either sync or async method.

        Args:
            text: The processed text content of the message.
            extractedData: The consolidated, structured data from the event.
            eventData: The original event payload, for context if needed.

        Returns:
            str: Simple response text
            OR
            Tuple[str, Union[str, Callable, Coroutine]]: Progressive response
            - First element: Quick response (immediate)
            - Second element: Detailed response (processed later)
        """
        pass

    # --- Progressive Fallback Support ---
    
    def _isProgressiveResponse(self, result: Any) -> bool:
        """
        Checks if the result is a progressive fallback response (tuple with 2 elements).
        
        Args:
            result: The result from _processMessage or _processSlashCommand
            
        Returns:
            True if it's a tuple with exactly 2 elements (quick, detailed)
        """
        return isinstance(result, tuple) and len(result) == 2
    
    async def _handleProgressiveResponse(self, result: tuple, extractedData: ExtractedEventData) -> str:
        """
        Handles progressive fallback responses by sending quick response immediately
        and then updating with detailed response.
        
        Args:
            result: Tuple containing (quick_response, detailed_response)
            extractedData: Event data for context
            
        Returns:
            The quick response for immediate sync response
        """
        quickResponse, detailedResponse = result
        
        # Schedule the detailed response to be processed and sent asynchronously
        asyncio.create_task(
            self._sendDetailedResponse(str(quickResponse), detailedResponse, extractedData)
        )
        
        # Return quick response for immediate sync response
        return str(quickResponse)
    
    async def _sendDetailedResponse(self, quickResponse: str, detailedResponse: Any, extractedData: ExtractedEventData):
        """
        Sends the detailed response as an update to the original message.
        
        Args:
            quickResponse: The quick response that was already sent
            detailedResponse: The detailed response (str or async callable)
            extractedData: Event data for context
        """
        try:
            # Get the detailed response
            if asyncio.iscoroutinefunction(detailedResponse):
                finalResponse = await detailedResponse()
            elif callable(detailedResponse):
                finalResponse = detailedResponse()
            else:
                finalResponse = str(detailedResponse)
            
            # Create a proper asyncio Task that's already completed
            async def completedCoroutine():
                return finalResponse
            
            # Create the task and let it complete immediately
            completedTask = asyncio.create_task(completedCoroutine())
            await completedTask  # Ensure it's completed
            
            # Use the existing async processor to update the message
            await self.asyncProcessor.handleAsyncResponse(completedTask, extractedData)
            
        except Exception as e:
            self.logger.exception(f"Error sending detailed progressive response: {e}") 