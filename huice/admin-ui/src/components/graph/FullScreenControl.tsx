/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZUall5WlE9PToyYTQ1YWU4Nw==

import { useFullScreen } from '@react-sigma/core'
import { MaximizeIcon, MinimizeIcon } from 'lucide-react'
import { controlButtonVariant } from '@/lib/constants'
import Button from '@/components/ui/Button'
import { useTranslation } from 'react-i18next'

/**
 * Component that toggles full screen mode.
 */
const FullScreenControl = () => {
  const { isFullScreen, toggle } = useFullScreen()
  const { t } = useTranslation()

  return (
    <>
      {isFullScreen ? (
        <Button variant={controlButtonVariant} onClick={toggle} tooltip={t('graphPanel.sideBar.fullScreenControl.windowed')} size="icon">
          <MinimizeIcon />
        </Button>
      ) : (
        <Button variant={controlButtonVariant} onClick={toggle} tooltip={t('graphPanel.sideBar.fullScreenControl.fullScreen')} size="icon">
          <MaximizeIcon />
        </Button>
      )}
    </>
  )
}
// NOTE  MS8yOmFIVnBZMlhsa0xUb3Y2bzZUall5WlE9PToyYTQ1YWU4Nw==

export default FullScreenControl