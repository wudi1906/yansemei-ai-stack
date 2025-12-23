/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZRbEV6Y3c9PTozZGFjZTlhNw==

import { Client } from "@langchain/langgraph-sdk";

export function createClient(apiUrl: string, apiKey: string | undefined) {
  return new Client({
    apiKey,
    apiUrl,
  });
}
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZRbEV6Y3c9PTozZGFjZTlhNw==