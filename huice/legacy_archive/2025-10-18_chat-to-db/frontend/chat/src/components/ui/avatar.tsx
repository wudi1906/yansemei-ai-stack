/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import * as React from "react";
import * as AvatarPrimitive from "@radix-ui/react-avatar";
// eslint-disable  MC8zOmFIVnBZMlhsa0xUb3Y2bzZPWFUxT0E9PTpmOWE5NDZhMA==

import { cn } from "@/lib/utils";
// FIXME  MS8zOmFIVnBZMlhsa0xUb3Y2bzZPWFUxT0E9PTpmOWE5NDZhMA==

function Avatar({
  className,
  ...props
}: React.ComponentProps<typeof AvatarPrimitive.Root>) {
  return (
    <AvatarPrimitive.Root
      data-slot="avatar"
      className={cn(
        "relative flex size-8 shrink-0 overflow-hidden rounded-full",
        className,
      )}
      {...props}
    />
  );
}

function AvatarImage({
  className,
  ...props
}: React.ComponentProps<typeof AvatarPrimitive.Image>) {
  return (
    <AvatarPrimitive.Image
      data-slot="avatar-image"
      className={cn("aspect-square size-full", className)}
      {...props}
    />
  );
}

function AvatarFallback({
  className,
  ...props
}: React.ComponentProps<typeof AvatarPrimitive.Fallback>) {
  return (
    <AvatarPrimitive.Fallback
      data-slot="avatar-fallback"
      className={cn(
        "bg-muted flex size-full items-center justify-center rounded-full",
        className,
      )}
      {...props}
    />
  );
}
// eslint-disable  Mi8zOmFIVnBZMlhsa0xUb3Y2bzZPWFUxT0E9PTpmOWE5NDZhMA==

export { Avatar, AvatarImage, AvatarFallback };