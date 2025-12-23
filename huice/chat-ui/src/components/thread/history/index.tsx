/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// @ts-expect-error  MC80OmFIVnBZMlhsa0xUb3Y2bzZURTVaV2c9PToxNGI0NTcyYQ==

import { Button } from "@/components/ui/button";
import { useThreads } from "@/providers/Thread";
import { Thread } from "@langchain/langgraph-sdk";
import { useEffect, useState } from "react";

import { getContentString } from "../utils";
import { useQueryState, parseAsBoolean } from "nuqs";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { PanelRightOpen, PanelRightClose, Trash2, MoreHorizontal } from "lucide-react";
import { useMediaQuery } from "@/hooks/useMediaQuery";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { useLanguage } from "@/providers/Language";
// TODO  MS80OmFIVnBZMlhsa0xUb3Y2bzZURTVaV2c9PToxNGI0NTcyYQ==

function ThreadList({
  threads,
  onThreadClick,
}: {
  threads: Thread[];
  onThreadClick?: (threadId: string) => void;
}) {
  const { t } = useLanguage();
  const [threadId, setThreadId] = useQueryState("threadId");
  const { deleteThread } = useThreads();
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [threadToDelete, setThreadToDelete] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDeleteClick = (e: React.MouseEvent, threadIdToDelete: string) => {
    e.stopPropagation();
    setThreadToDelete(threadIdToDelete);
    setDeleteDialogOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!threadToDelete) return;

    setIsDeleting(true);
    try {
      await deleteThread(threadToDelete);
      toast.success(t.deleteChat);

      // If we're deleting the current thread, clear the threadId
      if (threadToDelete === threadId) {
        setThreadId(null);
      }
    } catch (error) {
      console.error("Failed to delete thread:", error);
      toast.error(t.errorOccurred);
    } finally {
      setIsDeleting(false);
      setDeleteDialogOpen(false);
      setThreadToDelete(null);
    }
  };

  return (
    <>
      <div className="flex h-full w-full flex-col items-start justify-start gap-2 overflow-y-scroll [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-gray-300 [&::-webkit-scrollbar-track]:bg-transparent">
        {threads.map((thread) => {
          let itemText = thread.thread_id;
          if (
            typeof thread.values === "object" &&
            thread.values &&
            "messages" in thread.values &&
            Array.isArray(thread.values.messages) &&
            thread.values.messages?.length > 0
          ) {
            const firstMessage = thread.values.messages[0];
            itemText = getContentString(firstMessage.content);
          }
          return (
            <div
              key={thread.thread_id}
              className={`w-full px-1 group rounded-lg transition-colors ${
                thread.thread_id === threadId
                  ? "bg-violet-50/50"
                  : "hover:bg-violet-50/30"
              }`}
            >
              <div className="flex items-center w-full relative">
                {/* 选中状态指示条 */}
                {thread.thread_id === threadId && (
                  <div className="absolute left-0 top-1 bottom-1 w-1 bg-gradient-to-b from-violet-500 to-indigo-600 rounded-r-full z-10" />
                )}

                <Button
                  variant="ghost"
                  className={`flex-1 items-start justify-start text-left font-normal min-w-0 transition-all ${
                    thread.thread_id === threadId
                      ? "bg-transparent text-violet-700 font-medium ml-2"
                      : "hover:bg-violet-100/50 ml-2 text-gray-900"
                  }`}
                  onClick={(e) => {
                    e.preventDefault();
                    onThreadClick?.(thread.thread_id);
                    if (thread.thread_id === threadId) return;
                    setThreadId(thread.thread_id);
                  }}
                >
                  <p className="truncate text-ellipsis">{itemText}</p>
                </Button>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem
                      className="text-red-600 focus:text-red-600"
                      onClick={(e) => handleDeleteClick(e, thread.thread_id)}
                    >
                      <Trash2 className="mr-2 h-4 w-4" />
                      {t.deleteChat}
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          );
        })}
      </div>

      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{t.deleteChat}</AlertDialogTitle>
            <AlertDialogDescription>
              {t.confirmDelete}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isDeleting}>{t.cancel}</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmDelete}
              disabled={isDeleting}
              className="bg-red-600 hover:bg-red-700"
            >
              {isDeleting ? t.loading : t.deleteChat}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
// NOTE  Mi80OmFIVnBZMlhsa0xUb3Y2bzZURTVaV2c9PToxNGI0NTcyYQ==

function ThreadHistoryLoading() {
  return (
    <div className="flex h-full w-full flex-col items-start justify-start gap-2 overflow-y-scroll [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-gray-300 [&::-webkit-scrollbar-track]:bg-transparent">
      {Array.from({ length: 30 }).map((_, i) => (
        <Skeleton
          key={`skeleton-${i}`}
          className="h-10 w-[280px]"
        />
      ))}
    </div>
  );
}
// NOTE  My80OmFIVnBZMlhsa0xUb3Y2bzZURTVaV2c9PToxNGI0NTcyYQ==

export default function ThreadHistory() {
  const { t } = useLanguage();
  const isLargeScreen = useMediaQuery("(min-width: 1024px)");
  const [chatHistoryOpen, setChatHistoryOpen] = useQueryState(
    "chatHistoryOpen",
    parseAsBoolean.withDefault(false),
  );

  const { getThreads, threads, setThreads, threadsLoading, setThreadsLoading } =
    useThreads();

  useEffect(() => {
    if (typeof window === "undefined") return;
    setThreadsLoading(true);
    getThreads()
      .then(setThreads)
      .catch(console.error)
      .finally(() => setThreadsLoading(false));
  }, []);

  return (
    <>
      <div className="shadow-inner-right hidden h-screen w-[300px] shrink-0 flex-col items-start justify-start gap-6 border-r-[1px] border-violet-200/60 lg:flex">
        <div className="flex w-full items-center justify-between px-4 pt-3 pb-2 border-b border-violet-100/60">
          <Button
            className="hover:bg-violet-100"
            variant="ghost"
            onClick={() => setChatHistoryOpen((p) => !p)}
          >
            {chatHistoryOpen ? (
              <PanelRightOpen className="size-5 text-violet-600" />
            ) : (
              <PanelRightClose className="size-5 text-violet-600" />
            )}
          </Button>
          <h1 className="text-lg font-semibold tracking-tight text-center flex-1 bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
            {t.chatHistory}
          </h1>
          <div className="w-10"></div>
        </div>
        {threadsLoading ? (
          <ThreadHistoryLoading />
        ) : (
          <ThreadList threads={threads} />
        )}
      </div>
      <div className="lg:hidden">
        <Sheet
          open={!!chatHistoryOpen && !isLargeScreen}
          onOpenChange={(open) => {
            if (isLargeScreen) return;
            setChatHistoryOpen(open);
          }}
        >
          <SheetContent
            side="left"
            className="flex lg:hidden"
          >
            <SheetHeader>
              <SheetTitle>{t.chatHistory}</SheetTitle>
            </SheetHeader>
            <ThreadList
              threads={threads}
              onThreadClick={() => setChatHistoryOpen((o) => !o)}
            />
          </SheetContent>
        </Sheet>
      </div>
    </>
  );
}