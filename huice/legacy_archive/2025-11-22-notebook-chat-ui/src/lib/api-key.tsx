/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZNR2h4WlE9PTowNjMzNzgzZg==

export function getApiKey(): string | null {
  try {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem("lg:chat:apiKey") ?? null;
  } catch {
    // no-op
  }

  return null;
}
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZNR2h4WlE9PTowNjMzNzgzZg==