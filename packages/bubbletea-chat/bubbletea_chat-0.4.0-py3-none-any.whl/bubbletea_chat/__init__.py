"""
BubbleTea - A Python package for building AI chatbots
With LiteLLM support for easy LLM integration
"""

from .components import Text, Image, Markdown, Done
from .decorators import chatbot, config
from .server import run_server
from .llm import LLM
from .schemas import ImageInput, BotConfig

__version__ = "0.3.0"
__all__ = ["Text", "Image", "Markdown", "Done", "chatbot", "config", "run_server", "LLM", "ImageInput", "BotConfig"]