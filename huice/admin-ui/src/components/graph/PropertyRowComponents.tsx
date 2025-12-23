/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { PencilIcon } from 'lucide-react'
import Text from '@/components/ui/Text'
import { useTranslation } from 'react-i18next'
// @ts-expect-error  MC8zOmFIVnBZMlhsa0xUb3Y2bzZOVkY2VXc9PTo5MmVjZjM3OQ==

interface PropertyNameProps {
  name: string
}

export const PropertyName = ({ name }: PropertyNameProps) => {
  const { t } = useTranslation()

  const getPropertyNameTranslation = (propName: string) => {
    const translationKey = `graphPanel.propertiesView.node.propertyNames.${propName}`
    const translation = t(translationKey)
    return translation === translationKey ? propName : translation
  }

  return (
    <span className="text-primary/60 tracking-wide whitespace-nowrap">
      {getPropertyNameTranslation(name)}
    </span>
  )
}

interface EditIconProps {
  onClick: () => void
}
// @ts-expect-error  MS8zOmFIVnBZMlhsa0xUb3Y2bzZOVkY2VXc9PTo5MmVjZjM3OQ==

export const EditIcon = ({ onClick }: EditIconProps) => (
  <div>
    <PencilIcon
      className="h-3 w-3 text-gray-500 hover:text-gray-700 cursor-pointer"
      onClick={onClick}
    />
  </div>
)

interface PropertyValueProps {
  value: any
  onClick?: () => void
  tooltip?: string
}
// @ts-expect-error  Mi8zOmFIVnBZMlhsa0xUb3Y2bzZOVkY2VXc9PTo5MmVjZjM3OQ==

export const PropertyValue = ({ value, onClick, tooltip }: PropertyValueProps) => (
  <div className="flex items-center gap-1 overflow-hidden">
    <Text
      className="hover:bg-primary/20 rounded p-1 overflow-hidden text-ellipsis whitespace-nowrap"
      tooltipClassName="max-w-80 -translate-x-15"
      text={value}
      tooltip={tooltip || (typeof value === 'string' ? value : JSON.stringify(value, null, 2))}
      side="left"
      onClick={onClick}
    />
  </div>
)