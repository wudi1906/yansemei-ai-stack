/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC80OmFIVnBZMlhsa0xUb3Y2bzZZM1JRTVE9PTo3Mjg5MjJiOQ==

import { Plus, X, SquarePen, Send } from "lucide-react";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { ContentBlock } from "@langchain/core/messages";
import { useRef, useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import ThreadHistory from "./history";
import { useSourceAgent } from "@/hooks/use-source-agent";
// eslint-disable  MS80OmFIVnBZMlhsa0xUb3Y2bzZZM1JRTVE9PTo3Mjg5MjJiOQ==

interface SourcesPanelProps {
  contentBlocks: ContentBlock.Multimodal.Data[];
  onFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onRemoveBlock: (index: number) => void;
  onNewChat?: () => void;
}
// TODO  Mi80OmFIVnBZMlhsa0xUb3Y2bzZZM1JRTVE9PTo3Mjg5MjJiOQ==

export function SourcesPanel({
  contentBlocks,
  onFileUpload,
  onRemoveBlock,
  onNewChat,
}: SourcesPanelProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [activeTab, setActiveTab] = useState<"sources" | "history">("sources");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { sendFilesToSourceAgent } = useSourceAgent();

  const getBlockName = (block: ContentBlock.Multimodal.Data): string => {
    if (block.type === "file") {
      return block.metadata?.filename || "PDF";
    }
    if (block.type === "image") {
      return block.metadata?.name || "Image";
    }
    return "Unknown";
  };

  const getBlockIcon = (block: ContentBlock.Multimodal.Data): string => {
    if (block.type === "file") {
      return "📄";
    }
    if (block.type === "image") {
      return "🖼️";
    }
    return "📎";
  };

  const handleConfirmFiles = async () => {
    if (contentBlocks.length === 0) return;

    setIsSubmitting(true);
    try {
      const success = await sendFilesToSourceAgent(contentBlocks);
      if (success) {
        // Clear the files after successful submission
        // You can uncomment this if you want to auto-clear after submission
        // onRemoveBlock(-1); // This would need to be modified to clear all
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex h-full flex-col bg-white overflow-hidden">
      {/* Header with New Chat Button */}
      <div className="border-b border-gray-200 bg-white px-4 py-3">
        <div className="flex items-center justify-between gap-2">
          <h2 className="text-sm font-semibold text-gray-900">本页</h2>
          <Button
            variant="ghost"
            size="sm"
            className="h-8 w-8 p-0 hover:bg-gray-100"
            onClick={onNewChat}
            title="新对话"
          >
            <SquarePen className="size-4" />
          </Button>
        </div>
      </div>

      {/* Tabs */}
      <Tabs
        value={activeTab}
        onValueChange={(value) => setActiveTab(value as "sources" | "history")}
        className="flex flex-1 flex-col overflow-hidden"
      >
        <TabsList className="grid w-full grid-cols-2 rounded-none border-b border-gray-200 bg-white p-0">
          <TabsTrigger
            value="sources"
            className="rounded-none border-b-2 border-transparent bg-white text-gray-600 data-[state=active]:border-gray-900 data-[state=active]:bg-white data-[state=active]:text-gray-900"
          >
            来源
          </TabsTrigger>
          <TabsTrigger
            value="history"
            className="rounded-none border-b-2 border-transparent bg-white text-gray-600 data-[state=active]:border-gray-900 data-[state=active]:bg-white data-[state=active]:text-gray-900"
          >
            历史
          </TabsTrigger>
        </TabsList>

        {/* Sources Tab */}
        <TabsContent value="sources" className="flex flex-1 flex-col overflow-hidden bg-white">
          {/* Add Source Button */}
          <div className="border-b border-gray-200 bg-white p-3">
            <Label
              htmlFor="sources-file-input"
              className="flex cursor-pointer items-center justify-center gap-2 rounded-lg border border-dashed border-gray-300 bg-white px-4 py-3 transition-colors hover:bg-gray-50"
            >
              <Plus className="size-5 text-gray-600" />
              <span className="text-sm font-medium text-gray-600">+ 添加来源</span>
            </Label>
            <input
              id="sources-file-input"
              ref={fileInputRef}
              type="file"
              onChange={onFileUpload}
              multiple
              accept="image/jpeg,image/png,image/gif,image/webp,application/pdf"
              className="hidden"
            />
          </div>

          {/* Sources List */}
          <div className="flex-1 overflow-y-auto bg-white p-3">
            {contentBlocks.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <p className="text-center text-sm text-gray-500">
                  还没有添加来源
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {contentBlocks.map((block, index) => (
                  <div
                    key={index}
                    className="group flex items-center justify-between rounded-lg bg-gray-50 p-3 transition-colors hover:bg-gray-100"
                  >
                    <div className="flex items-center gap-2 min-w-0 flex-1">
                      <span className="text-lg flex-shrink-0">
                        {getBlockIcon(block)}
                      </span>
                      <span className="truncate text-sm text-gray-700">
                        {getBlockName(block)}
                      </span>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="ml-2 h-6 w-6 p-0 opacity-0 transition-opacity group-hover:opacity-100"
                      onClick={() => onRemoveBlock(index)}
                    >
                      <X className="size-4 text-gray-500" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Confirm Button */}
          {contentBlocks.length > 0 && (
            <div className="border-t border-gray-200 bg-white p-3">
              <Button
                onClick={handleConfirmFiles}
                disabled={isSubmitting}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                <Send className="size-4 mr-2" />
                {isSubmitting ? "发送中..." : "确认"}
              </Button>
            </div>
          )}
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history" className="flex flex-1 flex-col overflow-hidden bg-white">
          <div className="flex-1 overflow-hidden">
            <ThreadHistory />
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

// TODO  My80OmFIVnBZMlhsa0xUb3Y2bzZZM1JRTVE9PTo3Mjg5MjJiOQ==