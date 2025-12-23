/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import * as React from "react";
import * as SeparatorPrimitive from "@radix-ui/react-separator";
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZaV1ZCUmc9PTpiYjIyOWYzOQ==

import { cn } from "@/lib/utils";
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZaV1ZCUmc9PTpiYjIyOWYzOQ==

function Separator({
  className,
  orientation = "horizontal",
  decorative = true,
  ...props
}: React.ComponentProps<typeof SeparatorPrimitive.Root>) {
  return (
    <SeparatorPrimitive.Root
      data-slot="separator-root"
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "bg-border shrink-0 data-[orientation=horizontal]:h-px data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-px",
        className,
      )}
      {...props}
    />
  );
}

export { Separator };