/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZUV1JxWlE9PTpkZmIyYzMwMw==

import { cn } from "@/lib/utils";

function Skeleton({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="skeleton"
      className={cn("bg-primary/10 animate-pulse rounded-md", className)}
      {...props}
    />
  );
}
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZUV1JxWlE9PTpkZmIyYzMwMw==

export { Skeleton };