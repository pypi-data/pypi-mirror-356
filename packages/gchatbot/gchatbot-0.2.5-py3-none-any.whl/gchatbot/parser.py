import logging
import pprint
from typing import Optional
from .types import (
    ChatData,
    ChatMessage,
    EventPayload,
    ExtractedEventData,
    ParsedBasics,
    ParsedCommand,
)

logger = logging.getLogger(__name__)


class EventParser:
    """
    Handles parsing of various Google Chat event payloads.
    """

    def __init__(self, botName: str):
        """
        Initializes the EventParser.

        Args:
            botName: The configured name of the bot, used for parsing mentions.
        """
        self.botName = botName

    def extractEventData(self, eventData: EventPayload) -> Optional[ExtractedEventData]:
        """
        Orchestrates the parsing of various Google Chat event payload structures.

        It identifies the payload type, delegates to a specific `_parse_*` method,
        and then combines the basic info (user, space, message) with details
        from command/argument parsing.

        Args:
            eventData: The raw JSON payload dictionary from the Google Chat event.

        Returns:
            An `ExtractedEventData` dictionary containing the final, consolidated data,
            or `None` if essential data (like the user) cannot be parsed.
        """
        parsedBasics: Optional[ParsedBasics] = None
        try:
            if 'chat' in eventData:
                chatData = eventData['chat']
                if 'appCommandPayload' in chatData:
                    logger.debug("Parsing structure: App Command Payload")
                    parsedBasics = self._parseAppCommandPayload(eventData)
                elif 'messagePayload' in chatData:
                    logger.debug("Parsing structure: Message Payload")
                    parsedBasics = self._parseMessagePayload(chatData)
                else:
                    logger.debug("Parsing structure: Unstructured Chat Event")
                    parsedBasics = self._parseUnstructuredChatEvent(chatData, eventData)
            elif 'message' in eventData:
                logger.debug("Parsing structure: Direct Message/Webhook Event")
                parsedBasics = self._parseDirectMessageEvent(eventData)
            else:
                logger.debug("Parsing structure: Fallback Event")
                parsedBasics = self._parseFallbackEvent(eventData)

            if not parsedBasics:
                logger.warning("Failed to parse basic event structure (parsing failed). Cannot extract data.")
                return None

            user = parsedBasics.get('user')
            if not user:
                logger.warning("Failed to parse basic event structure (user missing). Cannot extract data.")
                return None

            message = parsedBasics.get('message', {})
            space = parsedBasics.get('space', {})
            isDirectMessageEvent = parsedBasics.get('isDirectMessageEvent', False)
            isFallbackEvent = parsedBasics.get('isFallback', False)

            userEmail = user.get('email', 'Unknown Email')
            userDisplayName = user.get('displayName', 'Unknown User')
            spaceName = space.get('name') if space else 'Unknown Space'
            if not spaceName:
                spaceName = 'Unknown Space'
                if not isFallbackEvent:
                    logger.warning("Could not determine space name from parsed data.")

            commandData: Optional[ParsedCommand] = None
            if not isFallbackEvent and message:
                commandData = self._parseCommandAndArguments(message)
                if commandData is None:
                    logger.error("Failed to parse command and arguments from message content.")
                    return None
            else:
                if isFallbackEvent:
                    logger.debug("Fallback event type detected: Skipping command/argument parsing.")
                else:
                    logger.warning("Message data missing or empty: Skipping command/argument parsing.")
                commandData = {"command": None, "arguments": "", "processedText": "", "rawText": ""}

            extracted: ExtractedEventData = {
                "rawText": commandData["rawText"],
                "processedText": commandData["processedText"],
                "command": commandData["command"],
                "arguments": commandData["arguments"],
                "userEmail": userEmail,
                "userDisplayName": userDisplayName,
                "spaceName": spaceName,
                "isDirectMessageEvent": isDirectMessageEvent,
                "messageName": message.get("name"),
                "isFallbackEvent": isFallbackEvent,
            }
            if logger.isEnabledFor(logging.INFO):
                 logger.debug(f"Event data extracted successfully:\n{pprint.pformat(extracted)}")
            return extracted
        except Exception as e:
            logger.exception(f"Critical error during event data extraction: {e}")
            return None

    def _parseAppCommandPayload(self, eventData: EventPayload) -> Optional[ParsedBasics]:
        try:
            chatData = eventData.get('chat', {})
            payload = chatData.get('appCommandPayload', {})
            if not payload: return None

            message = payload.get('message', {})
            user = message.get('sender')
            if not user:
                logger.debug("Sender not in message (appCommandPayload), falling back to eventData['user'].")
                user = eventData.get('user')

            space = message.get('space', payload.get('space'))

            if not user or not space:
                 logger.warning("User or Space data missing in 'appCommandPayload' structure.")
                 return None

            return {"message": message, "user": user, "space": space, "isDirectMessageEvent": False}
        except Exception as e:
            logger.exception(f"Error parsing app command payload: {e}")
            return None

    def _parseMessagePayload(self, chatData: ChatData) -> Optional[ParsedBasics]:
        try:
            payload = chatData.get('messagePayload', {})
            if not payload: return None

            user = chatData.get('user')
            message = payload.get('message', {})
            space = message.get('space')

            if not user or not message or not space:
                 logger.warning("User, Message or Space data missing in 'messagePayload' structure.")
                 return None

            return {"message": message, "user": user, "space": space, "isDirectMessageEvent": False}
        except Exception as e:
            logger.exception(f"Error parsing message payload: {e}")
            return None

    def _parseDirectMessageEvent(self, eventData: EventPayload) -> Optional[ParsedBasics]:
        try:
            message = eventData.get('message')
            user = eventData.get('user')
            space = eventData.get('space')

            if not message or not user or not space:
                 logger.warning("Message, User or Space data missing in direct message/webhook structure.")
                 return None

            isDirectMessageEvent = space.get('type') == 'DM'
            return {"message": message, "user": user, "space": space, "isDirectMessageEvent": isDirectMessageEvent}
        except Exception as e:
            logger.exception(f"Error parsing direct message/webhook payload: {e}")
            return None

    def _parseUnstructuredChatEvent(self, chatData: ChatData, eventData: EventPayload) -> Optional[ParsedBasics]:
        logger.debug(f"Unrecognized structure within 'chat' key: {list(chatData.keys())}. Attempting fallback parsing.")
        try:
            user = eventData.get('user')
            message = eventData.get('message', {})
            space = message.get('space', eventData.get('space'))

            if not message or not user:
                logger.warning("Could not find sufficient user or message data in unstructured 'chat' event.")
                return None

            return {"message": message, "user": user, "space": space or {}, "isDirectMessageEvent": False}
        except Exception as e:
             logger.exception(f"Error parsing unstructured chat event: {e}")
             return None

    def _parseFallbackEvent(self, eventData: EventPayload) -> Optional[ParsedBasics]:
        logger.debug(f"Unrecognized top-level event structure: {list(eventData.keys())}. Attempting minimal fallback parsing.")
        try:
            commonEvent = eventData.get('commonEventObject', {})
            user = commonEvent.get('user', eventData.get('user'))

            if not user:
                logger.error("Failed to identify user from event data in fallback.")
                return None

            logger.warning("Could not reliably determine message or space from fallback structure.")
            return {"message": {}, "user": user, "space": {}, "isDirectMessageEvent": False, "isFallback": True}
        except Exception as e:
            logger.exception(f"Error parsing fallback event: {e}")
            return None

    def _parseCommandAndArguments(self, message: ChatMessage) -> Optional[ParsedCommand]:
        try:
            rawText = message.get('text', '').strip()
            argumentTextUi = message.get('argumentText', '').strip()
            textToProcess = rawText
            annotations = message.get('annotations', [])

            command = None
            arguments = ""
            processedText = ""

            leadingBotMention = False
            for annotation in annotations:
                if (
                    annotation.get('type') == 'USER_MENTION' and
                    annotation.get('startIndex') == 0 and
                    annotation.get('userMention', {}).get('user', {}).get('type') == 'BOT'
                ):
                    textToProcess = argumentTextUi
                    leadingBotMention = True
                    logger.debug(f"Leading Bot mention found via annotation. Using argumentText for subsequent processing: '{textToProcess}'")
                    break

            if not leadingBotMention:
                mentionTrigger = f"@{self.botName}"
                if textToProcess.startswith(mentionTrigger):
                    textToProcess = textToProcess[len(mentionTrigger):].strip()
                    logger.debug(f"[Fallback] Bot mention detected via startswith. Processing text after mention: '{textToProcess}'")

            slashCommandAnnotation = None
            for annotation in annotations:
                if annotation.get('type') == 'SLASH_COMMAND' and 'slashCommand' in annotation:
                    slashCommandAnnotation = annotation['slashCommand']
                    logger.debug(f"Slash command found via UI annotation: {slashCommandAnnotation}")
                    break

            if slashCommandAnnotation:
                command = slashCommandAnnotation.get('commandName', '').strip('/')
                arguments = argumentTextUi
                processedText = arguments
                logger.debug(f"Parsed command from UI Annotation: command='{command}', arguments='{arguments}'")
            elif textToProcess.strip().startswith('/'):
                textToProcessStripped = textToProcess.strip()
                logger.debug(f"Potential manually typed slash command found (starts with '/'). Text being parsed: '{textToProcessStripped}'")
                parts = textToProcessStripped[1:].split(" ", 1)
                command = parts[0].lower()
                arguments = parts[1].strip() if len(parts) > 1 else ''
                processedText = arguments
                logger.debug(f"Parsed command from Manual Text: command='{command}', arguments='{arguments}'")
            else:
                logger.debug(f"Parsing as regular message (no command identified). Processed text: '{textToProcess}'")
                processedText = textToProcess
                arguments = processedText

            return {"command": command, "arguments": arguments, "processedText": processedText, "rawText": rawText}
        except Exception as e:
             logger.exception(f"Error parsing command and arguments: {e}")
             return None 