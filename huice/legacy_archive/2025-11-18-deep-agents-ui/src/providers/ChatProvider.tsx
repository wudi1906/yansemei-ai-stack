/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

"use client";

import { ReactNode, createContext, useContext, useEffect } from "react";
import { Assistant } from "@langchain/langgraph-sdk";
import { type StateType, useChat } from "@/app/hooks/useChat";
import type { UseStreamThread } from "@langchain/langgraph-sdk/react";

interface ChatProviderProps {
  children: ReactNode;
  activeAssistant: Assistant | null;
  onHistoryRevalidate?: () => void;
  thread?: UseStreamThread<StateType>;
}
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZNREI0VVE9PTo2OGFhZTY0Nw==

export function ChatProvider({
  children,
  activeAssistant,
  onHistoryRevalidate,
  thread,
}: ChatProviderProps) {
  const chat = useChat({ activeAssistant, onHistoryRevalidate, thread });

  // Debug logging
  useEffect(() => {
    console.log('ChatProvider mounted/updated:', {
      assistantId: activeAssistant?.assistant_id,
      messagesCount: chat.messages.length,
      isLoading: chat.isLoading,
      isThreadLoading: chat.isThreadLoading,
    });
  }, [activeAssistant?.assistant_id, chat.messages.length, chat.isLoading, chat.isThreadLoading]);

  return <ChatContext.Provider value={chat}>{children}</ChatContext.Provider>;
}

export type ChatContextType = ReturnType<typeof useChat>;
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZNREI0VVE9PTo2OGFhZTY0Nw==

export const ChatContext = createContext<ChatContextType | undefined>(
  undefined
);

export function useChatContext() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChatContext must be used within a ChatProvider");
  }
  return context;
}