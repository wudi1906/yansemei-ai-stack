/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZiVVkxVHc9PTo1YTAyMDYxMQ==

export function getApiKey(): string | null {
  try {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem("lg:chat:apiKey") ?? null;
  } catch {
    // no-op
  }

  return null;
}
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZiVVkxVHc9PTo1YTAyMDYxMQ==