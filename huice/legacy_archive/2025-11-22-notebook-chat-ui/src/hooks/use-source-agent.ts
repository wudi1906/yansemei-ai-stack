/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8zOmFIVnBZMlhsa0xUb3Y2bzZVak0wVVE9PTpmZGIwOTdkZQ==

import { toast } from "sonner";
import { ContentBlock } from "@langchain/core/messages";
import { Client } from "@langchain/langgraph-sdk";
import { getApiKey } from "@/lib/api-key";
// eslint-disable  MS8zOmFIVnBZMlhsa0xUb3Y2bzZVak0wVVE9PTpmZGIwOTdkZQ==

/**
 * Hook to handle source agent requests
 * When files are uploaded via the "添加来源" button, this hook sends them to the source agent
 */
export function useSourceAgent() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const sourceAgentId = process.env.NEXT_PUBLIC_SOURCE_AGENT_ID || "source_agent";

  const sendFilesToSourceAgent = async (
    contentBlocks: ContentBlock.Multimodal.Data[]
  ) => {
    if (!apiUrl) {
      toast.error("API URL not configured");
      return false;
    }

    try {
      // Create a LangGraph client
      const client = new Client({
        apiUrl,
        apiKey: getApiKey() ?? undefined,
      });

      // Create a new thread
      const thread = await client.threads.create();
      const threadId = thread.thread_id;

      // Prepare the message with files
      const message = {
        role: "user",
        content: contentBlocks,
      };

      // Submit the message to the source agent
      const run = await client.runs.create(threadId, sourceAgentId, {
        input: {
          messages: [message],
        },
      });

      toast.success("Files sent to source agent successfully");
      return true;
    } catch (error) {
      console.error("Error sending files to source agent:", error);
      toast.error("Failed to send files to source agent", {
        description:
          error instanceof Error ? error.message : "Unknown error occurred",
      });
      return false;
    }
  };

  return {
    sendFilesToSourceAgent,
  };
}

// FIXME  Mi8zOmFIVnBZMlhsa0xUb3Y2bzZVak0wVVE9PTpmZGIwOTdkZQ==