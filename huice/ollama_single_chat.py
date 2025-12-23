import os
import time

import httpx


def get_ollama_host() -> str:
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")


def get_model_name() -> str:
    return os.environ.get("OLLAMA_MODEL", "mistral-nemo:latest")


def chat(prompt: str, label: str) -> None:
    host = get_ollama_host()
    model = get_model_name()
    url = f"{host}/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    print(f"\n=== Test: {label} ===")
    print(f"Using host={host}, model={model}")
    t0 = time.perf_counter()
    try:
        resp = httpx.post(url, json=payload, timeout=120.0)
        dt = time.perf_counter() - t0
        print(f"[{label}] status={resp.status_code}, elapsed={dt:.2f}s")
        text = resp.text
        print(f"[{label}] response body (first 400 chars):\n{text[:400]}")
    except Exception as e:
        dt = time.perf_counter() - t0
        print(f"[{label}] request failed after {dt:.2f}s: {e}")


if __name__ == "__main__":
    chat("Say hello in English.", "short_prompt")

    mid_prompt = "请用中文详细总结下面这一段文本的要点：" + "这是一段模拟的产品说明文档。" * 50
    chat(mid_prompt, "medium_prompt")

    long_prompt = "请用中文提取出以下文本中的所有产品名和关键特性：" + "这是一段模拟的技术文档，非常长。" * 200
    chat(long_prompt, "long_prompt")
