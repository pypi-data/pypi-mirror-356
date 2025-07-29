import asyncio
import logging
from typing import Awaitable, Callable, Optional, Coroutine, Any
from google.apps import chat_v1 as google_chat
from .response import ResponseFactory
from .types import EventPayload, ExtractedEventData

logger = logging.getLogger(__name__)


class AsyncProcessor:
    """
    Handles the asynchronous processing of Google Chat events.
    This version uses a "monitor" pattern, waiting for a task to complete
    instead of re-running it.
    """

    def __init__(
        self,
        getAppCredentialsClient: Callable[[], Optional[google_chat.ChatServiceClient]],
        responseFactory: ResponseFactory,
    ):
        """
        Initializes the AsyncProcessor.

        Args:
            getAppCredentialsClient: A callable that returns an authenticated
                                        ChatServiceClient or None.
            responseFactory: An instance of ResponseFactory to create message cards.
        """
        self._getAppCredentialsClient = getAppCredentialsClient
        self.responseFactory = responseFactory

    async def runAndAndUpdate(self, coroutine: Coroutine[Any, Any, str], extractedData: ExtractedEventData):
        """
        Runs a given coroutine and then uses its result to update the chat message.
        This acts as a wrapper for handleAsyncResponse for progressive responses.

        Args:
            coroutine: The specific coroutine that will produce the detailed response string.
            extractedData: The consolidated data parsed from the event.
        """
        try:
            # Create a task from the coroutine so it can be passed to the handler
            processingTask = asyncio.create_task(coroutine)
            await self.handleAsyncResponse(processingTask, extractedData)
        except Exception as e:
            logger.exception(f"Error running the progressive response coroutine: {e}")

    async def handleAsyncResponse(self, processingTask: asyncio.Task, extractedData: ExtractedEventData):
        """
        The core asynchronous task that monitors an in-progress operation.

        This method posts an initial "Processing..." card, awaits the completion
        of the original processing task, and then updates the message with the
        final result or an error. It does NOT re-run the business logic.

        Args:
            processingTask: The asyncio Task for the original, in-progress processing.
            extractedData: The consolidated, structured data parsed from the event.
        """
        appClient = self._getAppCredentialsClient()
        spaceName = extractedData.get("spaceName")
        userDisplay = extractedData.get("userDisplayName", "User")

        if not appClient:
            logger.error(f"Cannot start async processing for space '{spaceName}': App client unavailable.")
            return
        if not spaceName or spaceName == 'Unknown Space':
            logger.error(f"Cannot start async processing: Invalid or missing 'spaceName'.")
            return

        processingMessageName = None
        try:
            # 1. Post "Processing..." message
            processingCardText = "🔄 Processing your request..."
            initialCard = self.responseFactory.createResponseCard(processingCardText, userDisplay)
            processingMessageReq = google_chat.CreateMessageRequest(
                parent=spaceName, message=google_chat.Message(cards_v2=[initialCard])
            )
            sentMessage = await asyncio.to_thread(appClient.create_message, request=processingMessageReq)
            processingMessageName = sentMessage.name
            logger.info(f"Sent 'Processing...' message ({processingMessageName}) to space {spaceName}")

            # 2. Wait for the original task to complete
            finalResponseText = await processingTask
            logger.debug(f"Core processing finished for {processingMessageName}.")

            # 3. Update the message with the final result
            finalCard = self.responseFactory.createResponseCard(finalResponseText, userDisplay)
            updateMessageReq = google_chat.UpdateMessageRequest(
                message=google_chat.Message(name=processingMessageName, cards_v2=[finalCard]),
                update_mask="cardsV2",
            )
            await asyncio.to_thread(appClient.update_message, request=updateMessageReq)
            logger.info(f"Successfully updated message {processingMessageName} in space {spaceName}.")

        except Exception as e:
            # This will catch errors from this method OR from the original task future.
            logger.exception(f"Error during async response handling for space {spaceName} (Msg: {processingMessageName}): {e}")
            if processingMessageName and appClient:
                try:
                    errorText = f"❌ An error occurred while processing your request: {type(e).__name__}"
                    errorCard = self.responseFactory.createResponseCard(errorText, userDisplay)
                    errorUpdateReq = google_chat.UpdateMessageRequest(
                        message=google_chat.Message(name=processingMessageName, cards_v2=[errorCard]),
                        update_mask="cardsV2",
                    )
                    await asyncio.to_thread(appClient.update_message, request=errorUpdateReq)
                    logger.info(f"Successfully updated message {processingMessageName} with error details.")
                except Exception as updateErr:
                    logger.exception(f"Failed to update message {processingMessageName} with error details: {updateErr}") 