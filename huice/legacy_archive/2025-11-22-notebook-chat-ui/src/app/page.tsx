/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

"use client";
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZUVXRTZFE9PTowZDU2ZDQ2OQ==

import { Thread } from "@/components/thread";
import { StreamProvider } from "@/providers/Stream";
import { ThreadProvider } from "@/providers/Thread";
import { ArtifactProvider } from "@/components/thread/artifact";
import { Toaster } from "@/components/ui/sonner";
import React from "react";
// TODO  MS8yOmFIVnBZMlhsa0xUb3Y2bzZUVXRTZFE9PTowZDU2ZDQ2OQ==

export default function DemoPage(): React.ReactNode {
  return (
    <React.Suspense fallback={<div>加载中...</div>}>
      <Toaster />
      <ThreadProvider>
        <StreamProvider>
          <ArtifactProvider>
            <Thread />
          </ArtifactProvider>
        </StreamProvider>
      </ThreadProvider>
    </React.Suspense>
  );
}