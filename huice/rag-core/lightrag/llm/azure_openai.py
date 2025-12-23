"""
Azure OpenAI compatibility layer.

This module provides backward compatibility by re-exporting Azure OpenAI functions
from the main openai module where the actual implementation resides.

All core logic for both OpenAI and Azure OpenAI now lives in lightrag.llm.openai,
with this module serving as a thin compatibility wrapper for existing code that
imports from lightrag.llm.azure_openai.
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# noqa  MC8yOmFIVnBZMlhsa0xUb3Y2bzZWSHBuUXc9PTo5MTVhYjgyZQ==

from lightrag.llm.openai import (
    azure_openai_complete_if_cache,
    azure_openai_complete,
    azure_openai_embed,
)
# noqa  MS8yOmFIVnBZMlhsa0xUb3Y2bzZWSHBuUXc9PTo5MTVhYjgyZQ==

__all__ = [
    "azure_openai_complete_if_cache",
    "azure_openai_complete",
    "azure_openai_embed",
]