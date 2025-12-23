/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZSbGR4T0E9PTo2NzhhZTJlMA==

export interface TabVisibilityContextType {
  visibleTabs: Record<string, boolean>;
  setTabVisibility: (tabId: string, isVisible: boolean) => void;
  isTabVisible: (tabId: string) => boolean;
}
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZSbGR4T0E9PTo2NzhhZTJlMA==