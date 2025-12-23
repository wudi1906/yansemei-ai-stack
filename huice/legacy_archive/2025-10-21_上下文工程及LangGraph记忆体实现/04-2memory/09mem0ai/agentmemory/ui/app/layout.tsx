import type React from "react";
import "@/app/globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { Navbar } from "@/components/Navbar";
import { Toaster } from "@/components/ui/toaster";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Providers } from "./providers";

export const metadata = {
  title: "智能记忆体 - 开发者仪表板",
  description: "管理您的智能记忆体集成和存储的记忆",
  generator: "v0.dev",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className="h-screen font-sans antialiased flex flex-col bg-zinc-950">
        <Providers>
          <ThemeProvider
            attribute="class"
            defaultTheme="dark"
            enableSystem
            disableTransitionOnChange
          >
            <Navbar />
            <ScrollArea className="h-[calc(100vh-64px)]">{children}</ScrollArea>
            <Toaster />
          </ThemeProvider>
        </Providers>
      </body>
    </html>
  );
}