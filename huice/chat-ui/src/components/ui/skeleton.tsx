/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { cn } from "@/lib/utils";
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZhRGhVUlE9PTo1YmY5ODUxYw==

function Skeleton({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="skeleton"
      className={cn("bg-primary/10 animate-pulse rounded-md", className)}
      {...props}
    />
  );
}

export { Skeleton };
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZhRGhVUlE9PTo1YmY5ODUxYw==