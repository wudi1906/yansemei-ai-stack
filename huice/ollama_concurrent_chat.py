import os
import time
import asyncio
import statistics

import httpx


def get_ollama_host() -> str:
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")


def get_model_name() -> str:
    return os.environ.get("OLLAMA_MODEL", "mistral-nemo:latest")


CONCURRENCY = 4
REQUESTS_PER_ROUND = 8


async def one_chat(client: httpx.AsyncClient, idx: int):
    host = get_ollama_host()
    model = get_model_name()
    url = f"{host}/api/chat"
    prompt = f"第 {idx} 个请求：请用一句话用中文总结一段产品说明。"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    t0 = time.perf_counter()
    try:
        resp = await client.post(url, json=payload)
        dt = time.perf_counter() - t0
        return idx, True, dt, resp.status_code, resp.text[:120]
    except Exception as e:
        dt = time.perf_counter() - t0
        return idx, False, dt, None, str(e)


async def main() -> None:
    host = get_ollama_host()
    model = get_model_name()
    print(f"Using host={host}, model={model}")
    print(f"CONCURRENCY={CONCURRENCY}, REQUESTS_PER_ROUND={REQUESTS_PER_ROUND}")

    limits = httpx.Limits(
        max_keepalive_connections=CONCURRENCY,
        max_connections=CONCURRENCY,
    )

    async with httpx.AsyncClient(timeout=120.0, limits=limits) as client:
        tasks = [one_chat(client, i) for i in range(REQUESTS_PER_ROUND)]
        results = await asyncio.gather(*tasks)

    ok_times = [r[2] for r in results if r[1]]
    failures = [r for r in results if not r[1]]

    print(f"\n=== Results ===")
    for idx, ok, dt, status, info in results:
        flag = "OK " if ok else "ERR"
        print(f"[{flag}] #{idx}: {dt:.2f}s, status={status}, info={info[:80]}")

    if ok_times:
        print("\nLatency summary (successful only):")
        print(
            "  count="
            + str(len(ok_times))
            + f" min={min(ok_times):.2f}s max={max(ok_times):.2f}s avg={statistics.mean(ok_times):.2f}s"
        )

    if failures:
        print(f"\nFailures: {len(failures)}")


if __name__ == "__main__":
    asyncio.run(main())
