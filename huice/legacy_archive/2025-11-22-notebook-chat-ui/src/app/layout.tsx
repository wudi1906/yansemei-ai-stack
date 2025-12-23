/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZUVmg0V1E9PTpjY2Q0MzNmYQ==

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
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZUVmg0V1E9PTpjY2Q0MzNmYQ==

export const metadata: Metadata = {
  title: "AuroraAINotebook",
  description: "Agent Chat UX",
};

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