/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC80OmFIVnBZMlhsa0xUb3Y2bzZlbU5rTUE9PTo3YTJmY2QxNA==

"use client";
// FIXME  MS80OmFIVnBZMlhsa0xUb3Y2bzZlbU5rTUE9PTo3YTJmY2QxNA==

import React, { useState, useEffect, Suspense, useRef } from "react";
import { useQueryState } from "nuqs";
import { getConfig, saveConfig, StandaloneConfig } from "@/lib/config";
import { ConfigDialog } from "@/app/components/ConfigDialog";
import { Button } from "@/components/ui/button";
import { Assistant } from "@langchain/langgraph-sdk";
import { ClientProvider } from "@/providers/ClientProvider";
import { Settings, MessagesSquare, SquarePen } from "lucide-react";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { ThreadList } from "@/app/components/ThreadList";
import { ChatProvider } from "@/providers/ChatProvider";
import { ChatInterface } from "@/app/components/ChatInterface";
// NOTE  Mi80OmFIVnBZMlhsa0xUb3Y2bzZlbU5rTUE9PTo3YTJmY2QxNA==

function HomePageContent() {
  const [config, setConfig] = useState<StandaloneConfig | null>(null);
  const [configDialogOpen, setConfigDialogOpen] = useState(false);
  const [debugMode, _] = useState(false);
  const [assistantId, setAssistantId] = useQueryState("assistantId");
  const [_threadId, setThreadId] = useQueryState("threadId");
  const [sidebar, setSidebar] = useQueryState("sidebar");

  const [mutateThreads, setMutateThreads] = useState<(() => void) | null>(null);
  const [interruptCount, setInterruptCount] = useState(0);

  // Use a stable key that only changes when user explicitly switches threads
  // This prevents re-mounting when a new thread is auto-created during message send
  const [chatKey, setChatKey] = useState<string>(() => _threadId || 'new-thread');
  const previousThreadIdRef = useRef<string | null>(_threadId);

  useEffect(() => {
    // Only update the key if threadId changed from a non-null value to another non-null value
    // or from non-null to null (new chat button clicked)
    // Don't update if it changed from null to non-null (auto-created thread)
    const prev = previousThreadIdRef.current;
    const current = _threadId;

    if (prev !== current) {
      console.log('Thread ID changed:', { prev, current });

      // User clicked "new chat" (non-null -> null)
      if (current === null) {
        const newKey = 'new-thread-' + Date.now();
        console.log('New chat clicked, setting key:', newKey);
        setChatKey(newKey);
      }
      // User selected a different existing thread (non-null -> different non-null)
      else if (prev !== null && current !== prev) {
        console.log('Switched to existing thread, setting key:', current);
        setChatKey(current);
      }
      // Auto-created thread (null -> non-null) - don't change key
      else if (prev === null && current !== null) {
        console.log('Auto-created thread, keeping key:', chatKey);
      }

      previousThreadIdRef.current = current;
    }
  }, [_threadId, chatKey]);

  // On mount, check for saved config, otherwise show config dialog
  useEffect(() => {
    const savedConfig = getConfig();
    if (savedConfig) {
      setConfig(savedConfig);
      if (!assistantId) {
        setAssistantId(savedConfig.assistantId);
      }
    } else {
      setConfigDialogOpen(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // If config changes, update the assistantId
  useEffect(() => {
    if (config && !assistantId) {
      setAssistantId(config.assistantId);
    }
  }, [config, assistantId, setAssistantId]);

  const handleSaveConfig = (newConfig: StandaloneConfig) => {
    saveConfig(newConfig);
    setConfig(newConfig);
  };

  const langsmithApiKey =
    config?.langsmithApiKey || process.env.NEXT_PUBLIC_LANGSMITH_API_KEY || "";

  if (!config) {
    return (
      <>
        <ConfigDialog
          open={configDialogOpen}
          onOpenChange={setConfigDialogOpen}
          onSave={handleSaveConfig}
        />
        <div className="flex h-screen items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold">欢迎使用智能对话平台</h1>
            <p className="mt-2 text-muted-foreground">
              配置您的部署以开始使用
            </p>
            <Button
              onClick={() => setConfigDialogOpen(true)}
              className="mt-4"
            >
              打开配置
            </Button>
          </div>
        </div>
      </>
    );
  }

  const assistant: Assistant = {
    assistant_id: config.assistantId,
    graph_id: config.assistantId,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    config: {},
    metadata: {},
    version: 1,
    name: "Default Assistant",
    context: {},
  };

  return (
    <>
      <ConfigDialog
        open={configDialogOpen}
        onOpenChange={setConfigDialogOpen}
        onSave={handleSaveConfig}
        initialConfig={config}
      />
      <ClientProvider
        deploymentUrl={config.deploymentUrl}
        apiKey={langsmithApiKey}
      >
        <div className="flex h-screen flex-col">
          <header className="flex h-16 items-center justify-between border-b border-border px-6">
            <div className="flex items-center gap-4">
              <h1 className="text-xl font-semibold">AuroraAI体平台</h1>
              {!sidebar && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSidebar("1")}
                  className="rounded-md border border-border bg-card p-3 text-foreground hover:bg-accent"
                >
                  <MessagesSquare className="mr-2 h-4 w-4" />
                  对话列表
                  {interruptCount > 0 && (
                    <span className="ml-2 inline-flex min-h-4 min-w-4 items-center justify-center rounded-full bg-destructive px-1 text-[10px] text-destructive-foreground">
                      {interruptCount}
                    </span>
                  )}
                </Button>
              )}
            </div>
            <div className="flex items-center gap-2">
              <div className="text-sm text-muted-foreground">
                <span className="font-medium">助手:</span>{" "}
                {config.assistantId}
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setConfigDialogOpen(true)}
              >
                <Settings className="mr-2 h-4 w-4" />
                设置
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setThreadId(null)}
                disabled={!_threadId}
                // Make this button the same teal as used elsewhere
                className="border-[#2F6868] bg-[#2F6868] text-white hover:bg-[#2F6868]/80"
              >
                <SquarePen className="mr-2 h-4 w-4" />
                新建对话
              </Button>
            </div>
          </header>

          <div className="flex-1 overflow-hidden">
            <ResizablePanelGroup
              direction="horizontal"
              autoSaveId="standalone-chat"
            >
              {sidebar && (
                <>
                  <ResizablePanel
                    id="thread-history"
                    order={1}
                    defaultSize={25}
                    minSize={20}
                    className="relative min-w-[380px]"
                  >
                    <ThreadList
                      onThreadSelect={async (id) => {
                        console.log('Selecting thread:', id);
                        await setThreadId(id);
                        console.log('Thread selected:', id);
                      }}
                      onMutateReady={(fn) => setMutateThreads(() => fn)}
                      onClose={() => setSidebar(null)}
                      onInterruptCountChange={setInterruptCount}
                    />
                  </ResizablePanel>
                  <ResizableHandle />
                </>
              )}

              <ResizablePanel
                id="chat"
                className="relative flex flex-col"
                order={2}
              >
                <ChatProvider
                  key={chatKey}
                  activeAssistant={assistant}
                  onHistoryRevalidate={() => mutateThreads?.()}
                >
                  <ChatInterface
                    assistant={assistant}
                    debugMode={debugMode}
                    controls={<></>}
                    skeleton={
                      <div className="flex items-center justify-center p-8">
                        <p className="text-muted-foreground">加载中...</p>
                      </div>
                    }
                  />
                </ChatProvider>
              </ResizablePanel>
            </ResizablePanelGroup>
          </div>
        </div>
      </ClientProvider>
    </>
  );
}

export default function HomePage() {
  return (
    <Suspense
      fallback={
        <div className="flex h-screen items-center justify-center">
          <p className="text-muted-foreground">加载中...</p>
        </div>
      }
    >
      <HomePageContent />
    </Suspense>
  );
}
// eslint-disable  My80OmFIVnBZMlhsa0xUb3Y2bzZlbU5rTUE9PTo3YTJmY2QxNA==