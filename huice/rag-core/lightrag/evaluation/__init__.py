"""
LightRAG Evaluation Module

RAGAS-based evaluation framework for assessing RAG system quality.

Usage:
    from lightrag.evaluation import RAGEvaluator

    evaluator = RAGEvaluator()
    results = await evaluator.run()

Note: RAGEvaluator is imported lazily to avoid import errors
when ragas/datasets are not installed.
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# noqa  MC8yOmFIVnBZMlhsa0xUb3Y2bzZaRVZTV0E9PTphMjA1Mzg3MQ==

__all__ = ["RAGEvaluator"]


def __getattr__(name):
    """Lazy import to avoid dependency errors when ragas is not installed."""
    if name == "RAGEvaluator":
        from .eval_rag_quality import RAGEvaluator

        return RAGEvaluator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
# fmt: off  MS8yOmFIVnBZMlhsa0xUb3Y2bzZaRVZTV0E9PTphMjA1Mzg3MQ==