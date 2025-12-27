/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZWalpGY3c9PTpjZDg0MDU3Ng==

"use client";

import { Thread } from "@/components/thread";
import { StreamProvider } from "@/providers/Stream";
import { ThreadProvider } from "@/providers/Thread";
import { LanguageProvider } from "@/providers/Language";
import { ArtifactProvider } from "@/components/thread/artifact";
import { Toaster } from "@/components/ui/sonner";
import { AuthGuard } from "@/components/AuthGuard";
import React from "react";

function LoadingFallback() {
  return <div className="flex h-screen items-center justify-center">Loading...</div>;
}

export default function DemoPage(): React.ReactNode {
  return (
    <React.Suspense fallback={<LoadingFallback />}>
      <AuthGuard>
        <Toaster />
        <LanguageProvider>
          <ThreadProvider>
            <StreamProvider>
              <ArtifactProvider>
                <Thread />
              </ArtifactProvider>
            </StreamProvider>
          </ThreadProvider>
        </LanguageProvider>
      </AuthGuard>
    </React.Suspense>
  );
}
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZWalpGY3c9PTpjZDg0MDU3Ng==