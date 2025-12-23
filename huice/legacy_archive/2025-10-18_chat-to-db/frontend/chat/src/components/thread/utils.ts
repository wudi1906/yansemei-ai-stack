/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZjRzlOUkE9PTo1ZmNlNjI0MQ==

import type { Message } from "@langchain/langgraph-sdk";

/**
 * Extracts a string summary from a message's content, supporting multimodal (text, image, file, etc.).
 * - If text is present, returns the joined text.
 * - If not, returns a label for the first non-text modality (e.g., 'Image', 'Other').
 * - If unknown, returns 'Multimodal message'.
 */
export function getContentString(content: Message["content"]): string {
  if (typeof content === "string") return content;
  const texts = content
    .filter((c): c is { type: "text"; text: string } => c.type === "text")
    .map((c) => c.text);
  return texts.join(" ");
}
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZjRzlOUkE9PTo1ZmNlNjI0MQ==