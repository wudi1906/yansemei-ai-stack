/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import type { Metadata } from "next";
import "./globals.css";
import { Inter } from "next/font/google";
import React from "react";
import { NuqsAdapter } from "nuqs/adapters/next/app";
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZSbVEyVWc9PToxMmYyYWI0Mg==

const inter = Inter({
  subsets: ["latin"],
  preload: true,
  display: "swap",
});

export const metadata: Metadata = {
  title: "AuroraAI企业级测试平台",
  description: "Agent Chat UX",
};
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZSbVEyVWc9PToxMmYyYWI0Mg==

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <NuqsAdapter>{children}</NuqsAdapter>
      </body>
    </html>
  );
}