import os
import time

import httpx


def get_ollama_host() -> str:
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")


def ping_tags() -> None:
    host = get_ollama_host()
    url = f"{host}/api/tags"
    t0 = time.perf_counter()
    try:
        resp = httpx.get(url, timeout=5.0)
        dt = time.perf_counter() - t0
        print(f"[TAGS] status={resp.status_code}, elapsed={dt:.3f}s")
        print(resp.text[:300])
    except Exception as e:
        dt = time.perf_counter() - t0
        print(f"[TAGS] request failed after {dt:.3f}s: {e}")


def ping_version() -> None:
    host = get_ollama_host()
    url = f"{host}/api/version"
    t0 = time.perf_counter()
    try:
        resp = httpx.get(url, timeout=5.0)
        dt = time.perf_counter() - t0
        print(f"[VERSION] status={resp.status_code}, elapsed={dt:.3f}s")
        print(resp.text[:300])
    except Exception as e:
        dt = time.perf_counter() - t0
        print(f"[VERSION] request failed after {dt:.3f}s: {e}")


if __name__ == "__main__":
    print("Using OLLAMA_HOST=", get_ollama_host())
    ping_tags()
    ping_version()
