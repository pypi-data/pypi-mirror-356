from typing import Any, Dict, List, Optional, TypedDict, Union, Tuple, Callable, Awaitable


# --- Type Definitions for Payloads and Extracted Data ---

class ChatUser(TypedDict, total=False):
    """
    Represents a user in Google Chat.
    The 'total=False' indicates that keys are optional.
    """
    name: str
    """The resource name of the user, e.g., "users/123456789"."""
    displayName: str
    """The user's display name."""
    avatarUrl: str
    """The URL for the user's avatar."""
    email: str
    """The user's email address."""
    type: str
    """The type of user, e.g., 'USER' or 'BOT'."""

class ChatSpace(TypedDict, total=False):
    """
    Represents a space (room or direct message) in Google Chat.
    The 'total=False' indicates that keys are optional.
    """
    name: str
    """The resource name of the space, e.g., "spaces/ABCDEFG"."""
    displayName: str
    """The display name of the space."""
    type: str
    """The type of space, e.g., 'DM' or 'ROOM'."""

class ChatMessageAnnotation(TypedDict, total=False):
    """
    Represents an annotation within a message, like a @mention or slash command.
    The 'total=False' indicates that keys are optional.
    """
    type: str
    """The type of annotation, e.g., 'USER_MENTION' or 'SLASH_COMMAND'."""
    startIndex: int
    """The starting index of the annotated text in the message."""
    length: int
    """The length of the annotated text."""
    userMention: Dict[str, Any]
    """If the annotation is a user mention, this field contains the user data."""
    slashCommand: Dict[str, Any]
    """If the annotation is a slash command, this field contains command data."""

class ChatMessage(TypedDict, total=False):
    """
    Represents a message sent in a Google Chat space.
    The 'total=False' indicates that keys are optional.
    """
    name: str
    """The resource name of the message, e.g., "spaces/ABC/messages/XYZ"."""
    sender: ChatUser
    """The user who sent the message."""
    createTime: str
    """The timestamp when the message was created."""
    text: str
    """The plain-text body of the message."""
    argumentText: str
    """The text that appears after a slash command or a bot mention."""
    thread: Dict[str, Any]
    """The thread the message belongs to."""
    space: ChatSpace
    """The space where the message was sent."""
    annotations: List[ChatMessageAnnotation]
    """A list of annotations in the message."""

class AppCommandPayload(TypedDict, total=False):
    """
    The payload specific to a slash command invocation from the Chat App UI.
    The 'total=False' indicates that keys are optional.
    """
    message: ChatMessage
    """The message object associated with the command."""
    space: ChatSpace
    """The space where the command was invoked."""

class ChatData(TypedDict, total=False):
    """
    A container for Chat-specific event data.
    The 'total=False' indicates that keys are optional.
    """
    appCommandPayload: AppCommandPayload
    """Payload for slash command events."""
    messagePayload: Dict[str, Any]
    """Payload for other message-related events."""
    user: ChatUser
    """The user associated with the event."""

class CommonEventObject(TypedDict, total=False):
    """
    A common structure for event metadata.
    The 'total=False' indicates that keys are optional.
    """
    user: ChatUser
    """The user who triggered the event."""

class EventPayload(TypedDict, total=False):
    """
    Represents the top-level structure of a raw event payload from Google Chat.
    The 'total=False' indicates that keys are optional.
    """
    type: str
    """The type of the event, e.g., 'MESSAGE', 'ADDED_TO_SPACE'."""
    eventTime: str
    """The timestamp when the event occurred."""
    chat: ChatData
    """Chat-specific data container."""
    message: ChatMessage
    """The message object, typically present in MESSAGE events."""
    user: ChatUser
    """The user who triggered the event."""
    space: ChatSpace
    """The space where the event occurred."""
    commonEventObject: CommonEventObject
    """Common metadata about the event."""

class ExtractedEventData(TypedDict):
    """
    Represents the consolidated, structured data extracted from an event payload.
    This type provides a clean, predictable interface for the bot's logic.
    """
    rawText: str
    """The original, unmodified text content from the message."""
    processedText: str
    """The text content relevant for processing (e.g., after removing a bot mention)."""
    command: Optional[str]
    """The identified slash command name, without the '/', or None if not a command."""
    arguments: str
    """The string of arguments that followed the slash command."""
    userEmail: str
    """The email address of the user who triggered the event."""
    userDisplayName: str
    """The display name of the user."""
    spaceName: str
    """The resource name of the space where the event occurred (e.g., "spaces/XXXX")."""
    isDirectMessageEvent: bool
    """True if the event occurred in a direct message (DM) with the bot."""
    messageName: Optional[str]
    """The resource name of the original message (e.g., "spaces/XXX/messages/YYY")."""
    isFallbackEvent: bool
    """True if the event payload structure was unrecognized and only minimal data could be parsed."""

class ParsedBasics(TypedDict, total=False):
    """
    An internal type used to store partially parsed event data before full extraction.
    The 'total=False' indicates that keys are optional.
    """
    message: ChatMessage
    """The parsed message object."""
    user: ChatUser
    """The parsed user object."""
    space: ChatSpace
    """The parsed space object."""
    isDirectMessageEvent: bool
    """Flag indicating if the event is a direct message."""
    isFallback: bool
    """Flag indicating if the parsing was a minimal fallback."""

class ParsedCommand(TypedDict):
    """An internal type to structure the results of command and argument parsing from text."""
    command: Optional[str]
    """The command name, or None."""
    arguments: str
    """The arguments string."""
    processedText: str
    """The text used for processing (arguments for commands, full text for messages)."""
    rawText: str
    """The original, unmodified text."""


# --- Type Aliases for Response Types ---

ProgressiveResponse = Tuple[str, Union[str, Callable[[], str], Callable[[], Awaitable[str]]]]
"""
Type alias for progressive responses.

A progressive response is a tuple containing:
- First element: Quick response (immediate feedback to user)
- Second element: Detailed response (can be a string, sync callable, or async callable)

Examples:
    # Simple progressive response
    ("⚡ Processing...", "✅ Complete!")
    
    # Progressive with sync callable
    ("⚡ Processing...", lambda: expensive_computation())
    
    # Progressive with async callable
    ("⚡ Processing...", async_function)
"""

ResponseType = Union[str, ProgressiveResponse]
"""
Type alias for all possible response types from bot methods.

Bot methods (_processMessage, _processSlashCommand) can return:
- str: Simple text response
- ProgressiveResponse: Tuple for two-stage responses (quick + detailed)

Examples:
    # Simple response
    return "Hello, world!"
    
    # Progressive response
    return ("⚡ Starting...", detailed_function)
""" 