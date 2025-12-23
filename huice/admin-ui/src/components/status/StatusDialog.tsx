/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { LightragStatus } from '@/api/lightrag'
import { useTranslation } from 'react-i18next'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/Dialog'
import StatusCard from './StatusCard'
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZRVGc1U3c9PTozNjZlY2Y1Nw==

interface StatusDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  status: LightragStatus | null
}

const StatusDialog = ({ open, onOpenChange, status }: StatusDialogProps) => {
  const { t } = useTranslation()

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>{t('graphPanel.statusDialog.title')}</DialogTitle>
          <DialogDescription>
            {t('graphPanel.statusDialog.description')}
          </DialogDescription>
        </DialogHeader>
        <StatusCard status={status} />
      </DialogContent>
    </Dialog>
  )
}

export default StatusDialog
// TODO  MS8yOmFIVnBZMlhsa0xUb3Y2bzZRVGc1U3c9PTozNjZlY2Y1Nw==