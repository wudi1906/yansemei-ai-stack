/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// TODO  MC80OmFIVnBZMlhsa0xUb3Y2bzZXSHBEZGc9PTowNTQ3YWE5Zg==

import Button from '@/components/ui/Button'
import { SiteInfo, webuiPrefix } from '@/lib/constants'
import AppSettings from '@/components/AppSettings'
import { TabsList, TabsTrigger } from '@/components/ui/Tabs'
import { useSettingsStore } from '@/stores/settings'
import { useAuthStore } from '@/stores/state'
import { cn } from '@/lib/utils'
import { useTranslation } from 'react-i18next'
import { navigationService } from '@/services/navigation'
import { Sparkles, LogOutIcon } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/Tooltip'
// TODO  MS80OmFIVnBZMlhsa0xUb3Y2bzZXSHBEZGc9PTowNTQ3YWE5Zg==

interface NavigationTabProps {
  value: string
  currentTab: string
  children: React.ReactNode
}

function NavigationTab({ value, currentTab, children }: NavigationTabProps) {
  return (
    <TabsTrigger
      value={value}
      className={cn(
        'cursor-pointer px-3 py-1.5 transition-all rounded-lg',
        currentTab === value ? '!bg-violet-500 !text-white shadow-md' : 'hover:bg-violet-100 dark:hover:bg-violet-900/30'
      )}
    >
      {children}
    </TabsTrigger>
  )
}
// eslint-disable  Mi80OmFIVnBZMlhsa0xUb3Y2bzZXSHBEZGc9PTowNTQ3YWE5Zg==

function TabsNavigation() {
  const currentTab = useSettingsStore.use.currentTab()
  const { t } = useTranslation()

  return (
    <div className="flex h-8 self-center">
      <TabsList className="h-full gap-2">
        <NavigationTab value="documents" currentTab={currentTab}>
          {t('header.documents')}
        </NavigationTab>
        <NavigationTab value="knowledge-graph" currentTab={currentTab}>
          {t('header.knowledgeGraph')}
        </NavigationTab>
        <NavigationTab value="retrieval" currentTab={currentTab}>
          {t('header.retrieval')}
        </NavigationTab>
        {/*<NavigationTab value="api" currentTab={currentTab}>*/}
        {/*  {t('header.api')}*/}
        {/*</NavigationTab>*/}
      </TabsList>
    </div>
  )
}

export default function SiteHeader() {
  const { t } = useTranslation()
  const { isGuestMode, apiVersion, username, webuiTitle, webuiDescription } = useAuthStore()
  // coreVersion
  // const versionDisplay = (coreVersion && apiVersion)
  //   ? `${coreVersion}/${apiVersion}`
  //   : null;
  const versionDisplay = null
  // Check if frontend needs rebuild (apiVersion ends with warning symbol)
  const hasWarning = apiVersion?.endsWith('⚠️');
  const versionTooltip = hasWarning
    ? t('header.frontendNeedsRebuild')
    : versionDisplay ? `v${versionDisplay}` : '';

  const handleLogout = () => {
    navigationService.navigateToLogin();
  }

  return (
    <header className="border-border/40 bg-gradient-to-r from-violet-50/90 via-white/95 to-indigo-50/90 dark:from-violet-950/50 dark:via-background/95 dark:to-indigo-950/50 supports-[backdrop-filter]:backdrop-blur-md sticky top-0 z-50 flex h-12 w-full border-b px-4 shadow-sm">
      <div className="min-w-[200px] w-auto flex items-center">
        <a href={webuiPrefix} className="flex items-center gap-2 group">
          <Sparkles className="size-5 text-violet-500 group-hover:text-amber-500 transition-colors" aria-hidden="true" />
          <span className="font-bold md:inline-block bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">{SiteInfo.name}</span>
        </a>
        {webuiTitle && (
          <div className="flex items-center">
            <span className="mx-1 text-xs text-gray-500 dark:text-gray-400">|</span>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <span className="font-medium text-sm cursor-default">
                    {webuiTitle}
                  </span>
                </TooltipTrigger>
                {webuiDescription && (
                  <TooltipContent side="bottom">
                    {webuiDescription}
                  </TooltipContent>
                )}
              </Tooltip>
            </TooltipProvider>
          </div>
        )}
      </div>

      <div className="flex h-10 flex-1 items-center justify-center">
        <TabsNavigation />
        {/*{isGuestMode && (*/}
        {/*  <div className="ml-2 self-center px-2 py-1 text-xs bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200 rounded-md">*/}
        {/*    {t('login.guestMode', 'Guest Mode')}*/}
        {/*  </div>*/}
        {/*)}*/}
      </div>

      <nav className="w-[200px] flex items-center justify-end">
        <div className="flex items-center gap-2">
          {versionDisplay && (
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <span className="text-xs text-gray-500 dark:text-gray-400 mr-1 cursor-default">
                    v{versionDisplay}
                  </span>
                </TooltipTrigger>
                <TooltipContent side="bottom">
                  {versionTooltip}
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          )}
          {/*<Button variant="ghost" size="icon" side="bottom" tooltip={t('header.projectRepository')}>*/}
          {/*  <a href={SiteInfo.github} target="_blank" rel="noopener noreferrer">*/}
          {/*    <GithubIcon className="size-4" aria-hidden="true" />*/}
          {/*  </a>*/}
          {/*</Button>*/}
          <AppSettings />
          {!isGuestMode && (
            <Button
              variant="ghost"
              size="icon"
              side="bottom"
              tooltip={`${t('header.logout')} (${username})`}
              onClick={handleLogout}
            >
              <LogOutIcon className="size-4" aria-hidden="true" />
            </Button>
          )}
        </div>
      </nav>
    </header>
  )
}
// eslint-disable  My80OmFIVnBZMlhsa0xUb3Y2bzZXSHBEZGc9PTowNTQ3YWE5Zg==