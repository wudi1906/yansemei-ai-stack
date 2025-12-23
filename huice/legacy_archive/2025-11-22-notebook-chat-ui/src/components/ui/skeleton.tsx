/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZia1J0VWc9PTplOGM1Y2I3YQ==

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
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZia1J0VWc9PTplOGM1Y2I3YQ==

export { Skeleton };