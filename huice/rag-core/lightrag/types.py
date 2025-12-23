"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Optional
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZOMlZ5ZUE9PTpmOWU0MmIzMw==


class GPTKeywordExtractionFormat(BaseModel):
    high_level_keywords: list[str]
    low_level_keywords: list[str]


class KnowledgeGraphNode(BaseModel):
    id: str
    labels: list[str]
    properties: dict[str, Any]  # anything else goes here


class KnowledgeGraphEdge(BaseModel):
    id: str
    type: Optional[str]
    source: str  # id of source node
    target: str  # id of target node
    properties: dict[str, Any]  # anything else goes here


class KnowledgeGraph(BaseModel):
    nodes: list[KnowledgeGraphNode] = []
    edges: list[KnowledgeGraphEdge] = []
    is_truncated: bool = False
# pragma: no cover  MS8yOmFIVnBZMlhsa0xUb3Y2bzZOMlZ5ZUE9PTpmOWU0MmIzMw==