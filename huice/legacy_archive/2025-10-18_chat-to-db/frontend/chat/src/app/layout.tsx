/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZNbWg0Tmc9PToyZWYwYjQyZg==

import type { Metadata } from "next";
import "./globals.css";
import { Inter } from "next/font/google";
import React from "react";
import { NuqsAdapter } from "nuqs/adapters/next/app";

const inter = Inter({
  subsets: ["latin"],
  preload: true,
  display: "swap",
});

export const metadata: Metadata = {
  title: "AuroraAI数据分析平台",
  description: "Agent Chat UX",
};
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZNbWg0Tmc9PToyZWYwYjQyZg==

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