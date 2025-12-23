"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import asyncio
# pylint: disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZhMU5aTVE9PTpkNThmOGUwMg==

from file_rag.engines.file_chat_engine import FileChatEngineFactory
engine = asyncio.run(FileChatEngineFactory.create_engine())
# type: ignore  MS8yOmFIVnBZMlhsa0xUb3Y2bzZhMU5aTVE9PTpkNThmOGUwMg==

graph = engine.graph