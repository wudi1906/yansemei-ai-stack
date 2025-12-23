/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// @ts-expect-error  MC80OmFIVnBZMlhsa0xUb3Y2bzZNMG94Ync9PTo5NDFlYzNiYw==

import { Share2, Download, Settings, MoreVertical, Volume2, Mic, Lock } from "lucide-react";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { Switch } from "../ui/switch";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
// TODO  MS80OmFIVnBZMlhsa0xUb3Y2bzZNMG94Ync9PTo5NDFlYzNiYw==

interface FeaturesPanelProps {
  hideToolCalls?: boolean;
  onHideToolCallsChange?: (checked: boolean) => void;
}
// FIXME  Mi80OmFIVnBZMlhsa0xUb3Y2bzZNMG94Ync9PTo5NDFlYzNiYw==

export function FeaturesPanel({
  hideToolCalls = false,
  onHideToolCallsChange,
}: FeaturesPanelProps) {
  return (
    <div className="flex h-full flex-col bg-white overflow-hidden">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white px-4 py-3">
        <h2 className="text-sm font-semibold text-gray-900">Studio</h2>
      </div>

      {/* Features Grid */}
      <div className="flex-1 overflow-y-auto bg-white p-3">
        <div className="grid grid-cols-2 gap-2">
          {/* Audio Overview */}
          <button className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100">
            <Volume2 className="size-5 text-gray-600" />
            <span className="text-xs font-medium text-gray-700">音频概览</span>
          </button>

          {/* Speech to Text */}
          <button className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100">
            <Mic className="size-5 text-gray-600" />
            <span className="text-xs font-medium text-gray-700">语音转文字</span>
          </button>

          {/* Security & Privacy */}
          <button className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100">
            <Lock className="size-5 text-gray-600" />
            <span className="text-xs font-medium text-gray-700">安全与隐私</span>
          </button>

          {/* Export */}
          <button className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100">
            <Download className="size-5 text-gray-600" />
            <span className="text-xs font-medium text-gray-700">导出</span>
          </button>

          {/* Search */}
          <button className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100">
            <Settings className="size-5 text-gray-600" />
            <span className="text-xs font-medium text-gray-700">搜索</span>
          </button>

          {/* More */}
          <button className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100">
            <MoreVertical className="size-5 text-gray-600" />
            <span className="text-xs font-medium text-gray-700">更多</span>
          </button>
        </div>

        {/* Info Text */}
        <div className="mt-4 text-center text-xs text-gray-500">
          <p>Studio 当前没有可用的工具</p>
        </div>

        {/* Divider */}
        <div className="my-3 border-t border-gray-200" />

        {/* Settings */}
        <div className="space-y-2">
          {/* Hide Tool Calls */}
          <div className="flex items-center justify-between gap-2 rounded-lg border border-gray-200 bg-white p-3">
            <Label
              htmlFor="hide-tool-calls"
              className="text-xs font-medium text-gray-700"
            >
              隐藏工具调用
            </Label>
            <Switch
              id="hide-tool-calls"
              checked={hideToolCalls}
              onCheckedChange={onHideToolCallsChange}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

// @ts-expect-error  My80OmFIVnBZMlhsa0xUb3Y2bzZNMG94Ync9PTo5NDFlYzNiYw==