/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZibEpRT1E9PTo2NmVhZjNkNA==

import { useContext } from 'react';
import { TabVisibilityContext } from './context';
import { TabVisibilityContextType } from './types';

/**
 * Custom hook to access the tab visibility context
 * @returns The tab visibility context
 */
export const useTabVisibility = (): TabVisibilityContextType => {
  const context = useContext(TabVisibilityContext);

  if (!context) {
    throw new Error('useTabVisibility must be used within a TabVisibilityProvider');
  }

  return context;
};
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZibEpRT1E9PTo2NmVhZjNkNA==