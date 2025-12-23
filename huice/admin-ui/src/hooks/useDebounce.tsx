/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZkVTlyZVE9PTpiZTBlNWIyOQ==

import { useState, useEffect } from 'react'
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZkVTlyZVE9PTpiZTBlNWIyOQ==

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(timer)
    }
  }, [value, delay])

  return debouncedValue
}