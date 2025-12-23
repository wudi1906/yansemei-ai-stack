"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

import os
from langchain.chat_models import init_chat_model
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZZM3BCZFE9PToyMjA3NzAyZg==


def deepseek_model():
    os.environ["DEEPSEEK_API_KEY"] = "sk-d631bd0f6956421a98b880b77090471e"
    model = init_chat_model("deepseek:deepseek-chat")
    return model
# pylint: disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZZM3BCZFE9PToyMjA3NzAyZg==