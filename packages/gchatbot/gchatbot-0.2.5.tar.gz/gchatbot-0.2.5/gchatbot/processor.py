import asyncio
import logging
from typing import Callable, Optional
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

    async def handleAsyncResponse(self, processing_task: asyncio.Task, extractedData: ExtractedEventData):
        """
        The core asynchronous task that monitors an in-progress operation.

        This method posts an initial "Processing..." card, awaits the completion
        of the original processing task, and then updates the message with the
        final result or an error. It does NOT re-run the business logic.

        Args:
            processing_task: The asyncio Task for the original, in-progress processing.
            extractedData: The consolidated, structured data parsed from the event.
        """
        appClient = self._getAppCredentialsClient()
        spaceName = extractedData.get("spaceName")
        userDisplay = extractedData.get("userDisplayName", "Usuário")

        if not appClient:
            logger.error(f"Cannot start async processing for space '{spaceName}': App client unavailable.")
            return
        if not spaceName or spaceName == 'Unknown Space':
            logger.error(f"Cannot start async processing: Invalid or missing 'spaceName'.")
            return

        processingMessageName = None
        try:
            # 1. Post "Processing..." message
            processingCardText = "🔄 Processando sua solicitação..."
            initialCard = self.responseFactory.createResponseCard(processingCardText, userDisplay)
            processingMessageReq = google_chat.CreateMessageRequest(
                parent=spaceName, message=google_chat.Message(cards_v2=[initialCard])
            )
            sentMessage = await asyncio.to_thread(appClient.create_message, request=processingMessageReq)
            processingMessageName = sentMessage.name
            logger.info(f"Sent 'Processing...' message ({processingMessageName}) to space {spaceName}")

            # 2. Wait for the original task to complete
            finalResponseText = await processing_task
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
                    errorText = f"❌ Ocorreu um erro ao processar sua solicitação: {type(e).__name__}"
                    errorCard = self.responseFactory.createResponseCard(errorText, userDisplay)
                    errorUpdateReq = google_chat.UpdateMessageRequest(
                        message=google_chat.Message(name=processingMessageName, cards_v2=[errorCard]),
                        update_mask="cardsV2",
                    )
                    await asyncio.to_thread(appClient.update_message, request=errorUpdateReq)
                    logger.info(f"Successfully updated message {processingMessageName} with error details.")
                except Exception as updateErr:
                    logger.exception(f"Failed to update message {processingMessageName} with error details: {updateErr}") 