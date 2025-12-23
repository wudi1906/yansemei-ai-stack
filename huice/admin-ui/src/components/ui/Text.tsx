/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZhbUZyYkE9PTo4MTFhMWJlNg==

import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/Tooltip'
import { cn } from '@/lib/utils'

const Text = ({
  text,
  className,
  tooltipClassName,
  tooltip,
  side,
  onClick
}: {
  text: string
  className?: string
  tooltipClassName?: string
  tooltip?: string
  side?: 'top' | 'right' | 'bottom' | 'left'
  onClick?: () => void
}) => {
  if (!tooltip) {
    return (
      <label
        className={cn(className, onClick !== undefined ? 'cursor-pointer' : undefined)}
        onClick={onClick}
      >
        {text}
      </label>
    )
  }

  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip>
        <TooltipTrigger asChild>
          <label
            className={cn(className, onClick !== undefined ? 'cursor-pointer' : undefined)}
            onClick={onClick}
          >
            {text}
          </label>
        </TooltipTrigger>
        <TooltipContent side={side} className={tooltipClassName}>
          {tooltip}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

export default Text
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZhbUZyYkE9PTo4MTFhMWJlNg==