/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZZMHhoWXc9PTpiN2RjZmRhMw==

import Button from '@/components/ui/Button'
import useTheme from '@/hooks/useTheme'
import { MoonIcon, SunIcon } from 'lucide-react'
import { useCallback } from 'react'
import { controlButtonVariant } from '@/lib/constants'
import { useTranslation } from 'react-i18next'
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZZMHhoWXc9PTpiN2RjZmRhMw==

/**
 * Component that toggles the theme between light and dark.
 */
export default function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const setLight = useCallback(() => setTheme('light'), [setTheme])
  const setDark = useCallback(() => setTheme('dark'), [setTheme])
  const { t } = useTranslation()

  if (theme === 'dark') {
    return (
      <Button
        onClick={setLight}
        variant={controlButtonVariant}
        tooltip={t('header.themeToggle.switchToLight')}
        size="icon"
        side="bottom"
      >
        <MoonIcon />
      </Button>
    )
  }
  return (
    <Button
      onClick={setDark}
      variant={controlButtonVariant}
      tooltip={t('header.themeToggle.switchToDark')}
      size="icon"
      side="bottom"
    >
      <SunIcon />
    </Button>
  )
}