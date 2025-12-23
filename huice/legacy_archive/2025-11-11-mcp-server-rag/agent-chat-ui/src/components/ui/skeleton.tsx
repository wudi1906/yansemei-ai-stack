/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZXbkZwYUE9PTo4N2YwY2IwNA==

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
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZXbkZwYUE9PTo4N2YwY2IwNA==

export { Skeleton };