/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { useContext } from 'react'
import { ThemeProviderContext } from '@/components/ThemeProvider'
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZTMkZyUXc9PTowNjE0ZjMwMA==

const useTheme = () => {
  const context = useContext(ThemeProviderContext)

  if (context === undefined) throw new Error('useTheme must be used within a ThemeProvider')

  return context
}

export default useTheme
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZTMkZyUXc9PTowNjE0ZjMwMA==