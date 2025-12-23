/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZRMVprZWc9PTowYzc0M2ViZA==

import { cn } from "@/lib/utils";

function Label({
  className,
  ...props
}: React.ComponentProps<typeof LabelPrimitive.Root>) {
  return (
    <LabelPrimitive.Root
      data-slot="label"
      className={cn(
        "flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
        className,
      )}
      {...props}
    />
  );
}

export { Label };
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZRMVprZWc9PTowYzc0M2ViZA==