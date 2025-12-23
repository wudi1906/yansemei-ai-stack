/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { useTheme } from "next-themes";
import { Toaster as Sonner, ToasterProps } from "sonner";
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZjM001YlE9PTpkMjhhYjEwYQ==

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme = "system" } = useTheme();

  return (
    <Sonner
      theme={theme as ToasterProps["theme"]}
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg",
          description: "group-[.toast]:text-muted-foreground",
          actionButton:
            "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground font-medium",
          cancelButton:
            "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground font-medium",
        },
      }}
      {...props}
    />
  );
};
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZjM001YlE9PTpkMjhhYjEwYQ==

export { Toaster };