"""
idea-cli: AI-Driven SDLC Engine

Transform project ideas into production-ready codebases through intelligent
validation, planning, and automated implementation with comprehensive demo mode
for immediate usage.

Key Features:
- Demo mode for immediate usage without API keys
- Multi-provider LLM support (Anthropic Claude, OpenAI GPT)
- Comprehensive error handling with automated issue reporting
- JSON schema validation for configuration management
- Progressive enhancement from demo to full mode

Usage:
    idea init-config     # Initialize configuration
    idea validate "..."  # Validate project idea
    idea new "..."       # Create scaffolded project
    idea run-queue       # Execute implementation queue
    idea report-issue    # Report bugs automatically

For more information, see the README.md file.
"""

__version__ = "0.2.0"
__author__ = "Claude Code"
__email__ = "claude@anthropic.com"
__description__ = "AI-Driven SDLC Engine with demo mode for immediate usage"

# Export main CLI for programmatic access
from .cli import app, main

__all__ = ["app", "main", "__version__"]
