/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 * 
 * Language Toggle Component for Chat UI
 */

"use client";

import { useLanguage } from '@/providers/Language';
import { Button } from './ui/button';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from './ui/tooltip';

export function LanguageToggle() {
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleLanguage}
            className="h-8 px-3 text-sm font-medium hover:bg-violet-100 hover:text-violet-700 transition-colors rounded-lg"
          >
            {language === 'zh' ? 'EN' : '中文'}
          </Button>
        </TooltipTrigger>
        <TooltipContent side="bottom" className="bg-violet-600 text-white border-violet-600">
          <p>{language === 'zh' ? t.switchToEnglish : t.switchToChinese}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
