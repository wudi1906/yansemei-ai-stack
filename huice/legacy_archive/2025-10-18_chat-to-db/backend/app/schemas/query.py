"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
# fmt: off  MC8yOmFIVnBZMlhsa0xUb3Y2bzZZbmRHWlE9PTo3ZmVkZjZmYw==


class QueryRequest(BaseModel):
    connection_id: int
    natural_language_query: str

# type: ignore  MS8yOmFIVnBZMlhsa0xUb3Y2bzZZbmRHWlE9PTo3ZmVkZjZmYw==

class QueryResponse(BaseModel):
    sql: str
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    context: Optional[Dict[str, Any]] = None  # For debugging/explanation