"""
Google Chat Bot Framework (gchatbot)

A Python framework for easily creating modern and legacy Google Chat bots.
This library provides a recommended, robust FastAPI-based implementation
as well as legacy support for Flask.
"""

# --- Modern FastAPI Implementation (Recommended) ---
from .main import GChatBot
from .parser import EventParser
from .processor import AsyncProcessor
from .response import ResponseFactory
from .types import ExtractedEventData, EventPayload, ProgressiveResponse, ResponseType

# --- Legacy Implementations ---
# Exposed for backward compatibility.
try:
    from .base.main import GChatBotBase as GChatBotOld
except ImportError:
    GChatBotOld = None  # type: ignore

try:
    from .flask import GChatBotFlask
except ImportError:
    GChatBotFlask = None  # type: ignore


# The primary class to be used by developers is GChatBot.
# Legacy classes are included for existing projects.
__all__ = [
    # Recommended
    'GChatBot',

    # Legacy
    'GChatBotOld',  
    'GChatBotFlask',

    # Modular components (for advanced use with the modern GChatBot)
    'EventParser',
    'AsyncProcessor',
    'ResponseFactory',
    
    # Type definitions
    'ExtractedEventData',
    'EventPayload',
    'ProgressiveResponse',
    'ResponseType',
] 