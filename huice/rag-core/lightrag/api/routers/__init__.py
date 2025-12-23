"""
This module contains all the routers for the LightRAG API.
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# noqa  MC8yOmFIVnBZMlhsa0xUb3Y2bzZSRFo2UWc9PTo2MDI5ZTYxYg==

from .document_routes import router as document_router
from .query_routes import router as query_router
from .graph_routes import router as graph_router
from .ollama_api import OllamaAPI

__all__ = ["document_router", "query_router", "graph_router", "OllamaAPI"]
# pragma: no cover  MS8yOmFIVnBZMlhsa0xUb3Y2bzZSRFo2UWc9PTo2MDI5ZTYxYg==