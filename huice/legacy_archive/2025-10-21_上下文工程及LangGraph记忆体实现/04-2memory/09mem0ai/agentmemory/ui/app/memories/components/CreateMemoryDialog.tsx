"use client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useState, useRef } from "react";
import { GoPlus } from "react-icons/go";
import { Loader2 } from "lucide-react";
import { useMemoriesApi } from "@/hooks/useMemoriesApi";
import { toast } from "sonner";
import { Textarea } from "@/components/ui/textarea";
import { t } from "@/lib/translations";

export function CreateMemoryDialog() {
  const { createMemory, isLoading, fetchMemories } = useMemoriesApi();
  const [open, setOpen] = useState(false);
  const textRef = useRef<HTMLTextAreaElement>(null);

  const handleCreateMemory = async (text: string) => {
    try {
      await createMemory(text);
      toast.success(t('dialogs.memoryCreatedSuccess'));
      // close the dialog
      setOpen(false);
      // refetch memories
      await fetchMemories();
    } catch (error) {
      console.error(error);
      toast.error(t('dialogs.memoryCreatedError'));
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="bg-primary hover:bg-primary/90 text-white"
        >
          <GoPlus />
          {t('nav.createMemory')}
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[525px] bg-zinc-900 border-zinc-800">
        <DialogHeader>
          <DialogTitle>{t('dialogs.createMemoryTitle')}</DialogTitle>
          <DialogDescription>
            {t('dialogs.createMemoryDescription')}
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="memory">{t('dialogs.memoryLabel')}</Label>
            <Textarea
              ref={textRef}
              id="memory"
              placeholder={t('dialogs.memoryPlaceholder')}
              className="bg-zinc-950 border-zinc-800 min-h-[150px]"
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            {t('common.cancel')}
          </Button>
          <Button
            disabled={isLoading}
            onClick={() => handleCreateMemory(textRef?.current?.value || "")}
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              t('dialogs.saveMemory')
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}