/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZSR1JMTmc9PTo4Mjk5YzRkYw==

import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
// TODO  MS8yOmFIVnBZMlhsa0xUb3Y2bzZSR1JMTmc9PTo4Mjk5YzRkYw==

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}