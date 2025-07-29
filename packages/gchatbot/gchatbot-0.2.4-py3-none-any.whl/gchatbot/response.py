import logging
import pprint
from typing import Any, Dict
from .types import EventPayload

logger = logging.getLogger(__name__)


class ResponseFactory:
    """
    A factory class responsible for creating and formatting bot responses.
    """

    def __init__(self, botName: str, botImageUrl: str):
        """
        Initializes the ResponseFactory.

        Args:
            botName: The display name of the bot.
            botImageUrl: The URL for the bot's avatar image.
        """
        self.botName = botName
        self.botImageUrl = botImageUrl

    def createResponseCard(self, cardText: str, userDisplayName: str) -> Dict[str, Any]:
        """
        Creates the standard card structure used for bot responses.
        This is used for both synchronous replies and asynchronous updates to maintain consistency.

        Args:
            cardText: The main text content for the card's body widget.
            userDisplayName: The display name of the user the response is directed to.

        Returns:
            A dictionary representing the JSON structure for a Google Chat card.
        """
        return {
            "card": {
                "header": {
                    "title": self.botName,
                    "subtitle": f"Para: {userDisplayName}",
                    "image_url": self.botImageUrl,
                    "image_type": "CIRCLE",
                    "image_alt_text": self.botName,
                },
                "sections": [
                    {
                        "widgets": [
                            {"text_paragraph": {"text": cardText}}
                        ]
                    }
                ],
            }
        }

    def formatSyncResponse(self, responseText: str, eventData: EventPayload) -> Dict[str, Any]:
        """
        Formats the response into the JSON structure expected by Google Chat API
        for synchronous replies.

        Args:
            responseText: The text content to be displayed in the response card.
            eventData: The original event payload from Google Chat.

        Returns:
            A dictionary with the properly formatted payload for a JSON response.
        """
        userInfo = eventData.get("user")
        if "chat" in eventData:
            userInfo = eventData.get("chat", {}).get("user", userInfo)
        userDisplayName = userInfo.get("displayName", "Usuário") if userInfo else "Usuário"

        responseCard = self.createResponseCard(responseText, userDisplayName)

        if "chat" in eventData:
            responsePayload = {
                "hostAppDataAction": {
                    "chatDataAction": {
                        "createMessageAction": {"message": {"cardsV2": [responseCard]}}
                    }
                }
            }
        else:
            responsePayload = {"cardsV2": [responseCard]}

        logger.debug(f"Sending response payload:\n {pprint.pformat(responsePayload)}")
        return responsePayload 