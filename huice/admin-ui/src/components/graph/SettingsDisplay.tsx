/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZia1o2ZEE9PTozZGE4YzRkOQ==

import { useSettingsStore } from '@/stores/settings'
import { useTranslation } from 'react-i18next'

/**
 * Component that displays current values of important graph settings
 * Positioned to the right of the toolbar at the bottom-left corner
 */
const SettingsDisplay = () => {
  const { t } = useTranslation()
  const graphQueryMaxDepth = useSettingsStore.use.graphQueryMaxDepth()
  const graphMaxNodes = useSettingsStore.use.graphMaxNodes()

  return (
    <div className="absolute bottom-4 left-[calc(1rem+2.5rem)] flex items-center gap-2 text-xs text-gray-400">
      <div>{t('graphPanel.sideBar.settings.depth')}: {graphQueryMaxDepth}</div>
      <div>{t('graphPanel.sideBar.settings.max')}: {graphMaxNodes}</div>
    </div>
  )
}
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZia1o2ZEE9PTozZGE4YzRkOQ==

export default SettingsDisplay