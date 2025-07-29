import asyncio
import json
import logging
import os
import pprint
import threading
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Union, Tuple, Callable, Awaitable, cast, TypeGuard, Coroutine

import google.oauth2.service_account
from fastapi import BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from google.apps import chat_v1 as google_chat

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

    This implementation uses a serverless-safe, hybrid processing model that
    leverages FastAPI's BackgroundTasks for long-running operations.
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
                 processingMessage: str = "🔄 Processing your request..."):
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
            processingMessage: The message to display while processing asynchronously.
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
            responseFactory=self.responseFactory
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

    # --- Synchronous Processing Wrapper ---

    def _processSyncEvent(self, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        Execute the core event processing logic for a synchronous handler.
        This is designed to be run in a separate thread to avoid blocking the event loop.

        Args:
            extractedData: The consolidated, structured data from the event.
            eventData: The original, raw event payload from Google Chat.

        Returns:
            The response (string or tuple) generated by the bot's processing logic.
        """
        # This function is now just a wrapper for _processEvent, ensuring it's called correctly.
        result = self._processEvent(extractedData, eventData)
        return result

    # --- Request Handling ---

    async def handleRequest(self, request: Request, backgroundTasks: BackgroundTasks) -> Any:
        """
        Main entry point for handling HTTP requests from Google Chat via FastAPI.
        This method is the core traffic controller, handling synchronous, asynchronous,
        and progressive responses in a serverless-safe way using FastAPI's BackgroundTasks.

        It works as follows:
        1.  Parses and validates the incoming request.
        2.  Determines if the designated handler (`_processMessage` or `_processSlashCommand`) is sync or async.
        3.  Executes the handler (in a thread if sync, directly if async).
        4.  Inspects the result from the handler:
            a.  If it's a simple string, a direct JSON response is returned.
            b.  If it's a "Progressive Response" (a tuple of `(quick_message, async_task)`),
                it immediately returns the `quick_message` and adds the `async_task`
                to FastAPI's background tasks for guaranteed execution.

        Args:
            request: The incoming FastAPI request object containing the Google Chat event payload.
            backgroundTasks: A FastAPI BackgroundTasks object to run tasks after responding.

        Returns:
            A `fastapi.responses.JSONResponse` with the immediate message payload.

        Raises:
            HTTPException: If the request method is not supported or an internal
                           error occurs during request parsing.
        """
        # 1. Handle GET requests for health checks
        if request.method == 'GET':
            self.logger.debug("Received GET request.")
            return JSONResponse(content={"status": "active", "message": f"{self.botName} is active. Use POST for events."})

        if request.method != 'POST':
            self.logger.warning(f"Received unsupported HTTP method: {request.method}")
            raise HTTPException(status_code=405, detail="Method Not Allowed")

        # 2. Parse and Validate POST request
        try:
            body = await request.body()
            if not body:
                self.logger.debug("Received empty payload. Returning 200 OK.")
                return JSONResponse(content={})
            eventData = json.loads(body)

            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"Received event data:\n{pprint.pformat(eventData)}")

            extractedData = self.eventParser.extractEventData(eventData)
            if not extractedData:
                self.logger.warning("Could not extract necessary data from the event. Returning 200 OK.")
                return JSONResponse(content={})

        except json.JSONDecodeError:
            self.logger.warning("Received invalid JSON payload. Returning 200 OK.")
            return JSONResponse(content={})
        except Exception as e:
            self.logger.exception("Error during initial request parsing.")
            raise HTTPException(status_code=500, detail="Error parsing incoming request.")

        # 3. Execute Processing Logic
        try:
            # Decide whether to run the sync or async event processor
            is_async_handler = (
                (extractedData.get("command") and inspect.iscoroutinefunction(self._processSlashCommand)) or
                (not extractedData.get("command") and inspect.iscoroutinefunction(self._processMessage))
            )

            if is_async_handler:
                # Await the async handler directly
                result = await self._processEventAsync(extractedData, eventData)
            else:
                # Run the sync handler in a thread to avoid blocking the event loop
                result = await asyncio.to_thread(self._processSyncEvent, extractedData, eventData)

            # 4. Handle the result
            if self._isProgressiveResponse(result):
                # This is a Progressive Response: (quick_message, detailed_response_coroutine)
                quick_response, detailed_coro = result
                self.logger.info("Progressive response detected. Sending quick response and scheduling detailed task.")

                # Schedule the detailed response task to run in the background
                backgroundTasks.add_task(
                    self.asyncProcessor.runAndAndUpdate,
                    # We cast here to satisfy the processor's more specific type hint.
                    # We know it's a Coroutine because that's what our handlers return.
                    coroutine=cast(Coroutine[Any, Any, str], detailed_coro),
                    extractedData=extractedData
                )

                # Return the initial "quick" response immediately
                response_payload = self.responseFactory.formatSyncResponse(str(quick_response), eventData)
                return JSONResponse(content=response_payload)
            else:
                # This is a simple, direct response
                self.logger.info("Simple response detected. Responding synchronously.")
                response_payload = self.responseFactory.formatSyncResponse(str(result), eventData)
                return JSONResponse(content=response_payload)

        except Exception as e:
            self.logger.exception("An unexpected error occurred during event processing.")
            error_message = "An error occurred while processing your request."
            response_payload = self.responseFactory.formatSyncResponse(error_message, eventData)
            return JSONResponse(content=response_payload, status_code=500)


    # --- Event Processing Router ---

    def _processEvent(self, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        Routes the event to the appropriate SYNCHRONOUS handler.
        This method should only be called for handlers that are not async.

        Args:
            extractedData: The dictionary of consolidated data.
            eventData: The original event payload for context.

        Returns:
            The response (string or tuple) from the specific handler.
        """
        command = extractedData.get("command")
        # Route based on whether a command was identified
        if command:
            self.logger.info(f"Routing to SYNC slash command handler: /{command}")
            arguments = extractedData.get("arguments", "")
            return self._processSlashCommand(command, arguments, extractedData, eventData)
        else:
            self.logger.info(f"Routing to SYNC message handler.")
            processedText = extractedData.get("processedText", "")
            return self._processMessage(processedText, extractedData, eventData)


    async def _processEventAsync(self, extractedData: ExtractedEventData, eventData: EventPayload) -> ResponseType:
        """
        Routes the event to the appropriate ASYNCHRONOUS handler.
        This method should only be called for handlers that are async.

        Args:
            extractedData: The dictionary of consolidated data.
            eventData: The original event payload for context.

        Returns:
            The response (string or tuple) from the specific handler.
        """
        command = extractedData.get("command")
        # Route based on whether a command was identified
        if command:
            self.logger.info(f"Routing to ASYNC slash command handler: /{command}")
            arguments = extractedData.get("arguments", "")
            # We cast here because the ABC defines a sync method, but our runtime check
            # in handleRequest ensures this is a coroutine function.
            coro = self._processSlashCommand(command, arguments, extractedData, eventData)
            return await cast(Awaitable[ResponseType], coro)
        else:
            self.logger.info(f"Routing to ASYNC message handler.")
            processedText = extractedData.get("processedText", "")
            # We cast here for the same reason as above.
            coro = self._processMessage(processedText, extractedData, eventData)
            return await cast(Awaitable[ResponseType], coro)


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
            Tuple[str, Awaitable[str]]: Progressive response
            - First element: Quick response text (immediate)
            - Second element: An awaitable (e.g., a coroutine) that returns the final detailed text.
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
            Tuple[str, Awaitable[str]]: Progressive response
            - First element: Quick response text (immediate)
            - Second element: An awaitable (e.g., a coroutine) that returns the final detailed text.
        """
        pass

    # --- Progressive Response Support ---

    def _isProgressiveResponse(self, result: Any) -> TypeGuard[ProgressiveResponse]:
        """
        Checks if the result from a handler is a progressive response.
        A progressive response is a tuple of (string, awaitable).
        """
        return (
            isinstance(result, tuple) and
            len(result) == 2 and
            isinstance(result[0], str) and
            inspect.isawaitable(result[1])
        )

    # The _handleProgressiveResponse and _sendDetailedResponse methods have been removed,
    # as their logic has been integrated directly into handleRequest using BackgroundTasks
    # for serverless-safe execution. 