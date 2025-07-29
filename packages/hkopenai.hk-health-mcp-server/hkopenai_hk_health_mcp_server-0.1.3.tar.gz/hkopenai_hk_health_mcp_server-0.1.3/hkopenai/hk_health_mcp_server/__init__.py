"""Hong Kong Health MCP Server package."""
from .app import main
from .tool_aed_waiting import get_aed_waiting_times

__version__ = "0.1.0"
__all__ = ['main', 'get_aed_waiting_times',]
