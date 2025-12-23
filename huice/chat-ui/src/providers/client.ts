/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZVMWRKYUE9PTphMzc5MmUwMg==

import { Client } from "@langchain/langgraph-sdk";
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZVMWRKYUE9PTphMzc5MmUwMg==

export function createClient(apiUrl: string, apiKey: string | undefined) {
  return new Client({
    apiKey,
    apiUrl,
  });
}