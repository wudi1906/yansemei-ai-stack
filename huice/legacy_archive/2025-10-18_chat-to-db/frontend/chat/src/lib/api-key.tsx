/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZhWGRNUkE9PTo4MzEyZGQ1ZQ==

export function getApiKey(): string | null {
  try {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem("lg:chat:apiKey") ?? null;
  } catch {
    // no-op
  }

  return null;
}
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZhWGRNUkE9PTo4MzEyZGQ1ZQ==