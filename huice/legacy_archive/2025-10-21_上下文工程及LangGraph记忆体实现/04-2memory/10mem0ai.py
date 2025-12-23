# https://mem0-4vmi.vercel.app/
# https://docs.mem0.ai/introduction#stateless-vs-stateful-agents
# https://docs.mem0.ai/components/llms/models/deepseek

# pip install mem0ai
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768,  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434",  # Ensure this URL is correct
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            # Alternatively, you can use "snowflake-arctic-embed:latest"
            "ollama_base_url": "http://localhost:11434",
        },
    },
}

# Initialize Memory with the configuration
m = Memory.from_config(config)

messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about a thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I'm not a big fan of thriller movies but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future."}
]

# Store inferred memories (default behavior)
result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"})

# Store memories with agent and run context
result = m.add(messages, user_id="alice", agent_id="movie-assistant", run_id="session-001", metadata={"category": "movie_recommendations"})

# Store raw messages without inference
# result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"}, infer=False)

result = m.add(messages, user_id="alice", metadata={"category": "preferences"})