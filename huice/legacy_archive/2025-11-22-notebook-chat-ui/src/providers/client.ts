/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZjRkJZZUE9PTowMjk2YzVmYQ==

import { Client } from "@langchain/langgraph-sdk";
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZjRkJZZUE9PTowMjk2YzVmYQ==

export function createClient(apiUrl: string, apiKey: string | undefined) {
  return new Client({
    apiKey,
    apiUrl,
  });
}