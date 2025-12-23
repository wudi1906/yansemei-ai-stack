/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZiRnBZTlE9PTowZDg0NmMzNg==

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZiRnBZTlE9PTowZDg0NmMzNg==