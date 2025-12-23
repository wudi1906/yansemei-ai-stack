/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZZMFp5Y3c9PTpjYTRjOWRkOQ==

import React from "react";
import type { OptimizedContentBlock } from "@/lib/multimodal-utils";
import { MultimodalPreview } from "./MultimodalPreview";
import { cn } from "@/lib/utils";

interface ContentBlocksPreviewProps {
  blocks: OptimizedContentBlock[];
  onRemove: (idx: number) => void;
  size?: "sm" | "md" | "lg";
  className?: string;
}
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZZMFp5Y3c9PTpjYTRjOWRkOQ==

/**
 * Renders a preview of content blocks with optional remove functionality.
 * Uses cn utility for robust class merging.
 */
export const ContentBlocksPreview: React.FC<ContentBlocksPreviewProps> = ({
  blocks,
  onRemove,
  size = "md",
  className,
}) => {
  if (!blocks.length) return null;
  return (
    <div className={cn("flex flex-wrap gap-2 p-3.5 pb-0", className)}>
      {blocks.map((block, idx) => (
        <MultimodalPreview
          key={idx}
          block={block}
          removable
          onRemove={() => onRemove(idx)}
          size={size}
        />
      ))}
    </div>
  );
};