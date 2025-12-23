/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZOMWR0U1E9PTo3M2E3MzYzNA==

import { Client } from "@langchain/langgraph-sdk";
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZOMWR0U1E9PTo3M2E3MzYzNA==

export function createClient(apiUrl: string, apiKey: string | undefined) {
  return new Client({
    apiKey,
    apiUrl,
  });
}