/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { useCallback } from 'react'
import { BookOpenIcon } from 'lucide-react'
import Button from '@/components/ui/Button'
import { controlButtonVariant } from '@/lib/constants'
import { useSettingsStore } from '@/stores/settings'
import { useTranslation } from 'react-i18next'
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZNVk5WZVE9PTo1ODcxZWQ2OQ==

/**
 * Component that toggles legend visibility.
 */
const LegendButton = () => {
  const { t } = useTranslation()
  const showLegend = useSettingsStore.use.showLegend()
  const setShowLegend = useSettingsStore.use.setShowLegend()

  const toggleLegend = useCallback(() => {
    setShowLegend(!showLegend)
  }, [showLegend, setShowLegend])

  return (
    <Button
      variant={controlButtonVariant}
      onClick={toggleLegend}
      tooltip={t('graphPanel.sideBar.legendControl.toggleLegend')}
      size="icon"
    >
      <BookOpenIcon />
    </Button>
  )
}
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZNVk5WZVE9PTo1ODcxZWQ2OQ==

export default LegendButton