/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZTVEZqVVE9PTpiMDhmZDM4Mg==

import { createContext } from 'react';
import { TabVisibilityContextType } from './types';

// Default context value
const defaultContext: TabVisibilityContextType = {
  visibleTabs: {},
  setTabVisibility: () => {},
  isTabVisible: () => false,
};

// Create the context
export const TabVisibilityContext = createContext<TabVisibilityContextType>(defaultContext);
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZTVEZqVVE9PTpiMDhmZDM4Mg==