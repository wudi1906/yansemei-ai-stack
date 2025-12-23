#!/bin/bash

# Setup Chat UI Environment
echo "Configuring Chat UI..."
cat > chat-ui/.env <<EOL
NEXT_PUBLIC_API_URL=http://localhost:2025
NEXT_PUBLIC_ASSISTANT_ID=chat_agent
EOL

# Setup Agent Service Environment
echo "Configuring Agent Service..."
cat > agent-service/.env <<EOL
# LLM Configuration - Gemini 2.5 Flash (新 API Key)
LLM_PROVIDER=google
GOOGLE_API_KEY=AIzaSyA-sa5B1NG4umHgtbzH-OsuJl_q1owC-I0
GOOGLE_MODEL=gemini-2.5-flash

# Alternative: DeepSeek
# LLM_PROVIDER=deepseek
# DEEPSEEK_API_KEY=sk-e995a95f08e14ff39904d41bbf54e742
EOL

echo "✅ Environment configuration complete."
echo "Installing dependencies..."
pip install langchain-google-genai

echo "🎉 Ready! Please restart your services with: python start_all.py"
