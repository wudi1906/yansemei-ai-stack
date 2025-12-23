"use client";

import { useState, useEffect } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SaveIcon, RotateCcw } from "lucide-react"
import { FormView } from "@/components/form-view"
import { JsonEditor } from "@/components/json-editor"
import { useConfig } from "@/hooks/useConfig"
import { useSelector } from "react-redux"
import { RootState } from "@/store/store"
import { useToast } from "@/components/ui/use-toast"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { t } from "@/lib/translations"

export default function SettingsPage() {
  const { toast } = useToast()
  const configState = useSelector((state: RootState) => state.config)
  const [settings, setSettings] = useState({
    openmemory: configState.openmemory || {
      custom_instructions: null
    },
    mem0: configState.mem0
  })
  const [viewMode, setViewMode] = useState<"form" | "json">("form")
  const { fetchConfig, saveConfig, resetConfig, isLoading, error } = useConfig()

  useEffect(() => {
    // Load config from API on component mount
    const loadConfig = async () => {
      try {
        await fetchConfig()
      } catch (error) {
        toast({
          title: t('errors.error'),
          description: t('settings.loadError'),
          variant: "destructive",
        })
      }
    }
    
    loadConfig()
  }, [])

  // Update local state when redux state changes
  useEffect(() => {
    setSettings(prev => ({
      ...prev,
      openmemory: configState.openmemory || { custom_instructions: null },
      mem0: configState.mem0
    }))
  }, [configState.openmemory, configState.mem0])

  const handleSave = async () => {
    try {
      await saveConfig({ 
        openmemory: settings.openmemory,
        mem0: settings.mem0 
      })
      toast({
        title: "设置已保存",
        description: t('settings.saveSuccess'),
      })
    } catch (error) {
      toast({
        title: t('errors.error'),
        description: t('settings.saveError'),
        variant: "destructive",
      })
    }
  }

  const handleReset = async () => {
    try {
      await resetConfig()
      toast({
        title: "设置已重置",
        description: t('settings.resetSuccess'),
      })
      await fetchConfig()
    } catch (error) {
      toast({
        title: t('errors.error'),
        description: t('settings.resetError'),
        variant: "destructive",
      })
    }
  }

  return (
    <div className="text-white py-6">
      <div className="container mx-auto py-10 max-w-4xl">
        <div className="flex justify-between items-center mb-8">
          <div className="animate-fade-slide-down">
            <h1 className="text-3xl font-bold tracking-tight">{t('settings.title')}</h1>
            <p className="text-muted-foreground mt-1">{t('settings.description')}</p>
          </div>
          <div className="flex space-x-2">
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="outline" className="border-zinc-800 text-zinc-200 hover:bg-zinc-700 hover:text-zinc-50 animate-fade-slide-down" disabled={isLoading}>
                  <RotateCcw className="mr-2 h-4 w-4" />
                  {t('settings.resetDefaults')}
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>{t('settings.resetConfirmTitle')}</AlertDialogTitle>
                  <AlertDialogDescription>
                    {t('settings.resetConfirmDescription')}
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>{t('settings.cancel')}</AlertDialogCancel>
                  <AlertDialogAction onClick={handleReset} className="bg-red-600 hover:bg-red-700">
                    {t('settings.resetConfirm')}
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
            
            <Button onClick={handleSave} className="bg-primary hover:bg-primary/90 animate-fade-slide-down" disabled={isLoading}>
              <SaveIcon className="mr-2 h-4 w-4" />
              {isLoading ? "保存中..." : t('settings.save')}
            </Button>
          </div>
        </div>

        <Tabs value={viewMode} onValueChange={(value) => setViewMode(value as "form" | "json")} className="w-full animate-fade-slide-down delay-1">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="form">{t('settings.formView')}</TabsTrigger>
            <TabsTrigger value="json">{t('settings.jsonEditor')}</TabsTrigger>
          </TabsList>

          <TabsContent value="form">
            <FormView settings={settings} onChange={setSettings} />
          </TabsContent>

          <TabsContent value="json">
            <Card>
              <CardHeader>
                <CardTitle>{t('settings.jsonConfiguration')}</CardTitle>
                <CardDescription>{t('settings.jsonDescription')}</CardDescription>
              </CardHeader>
              <CardContent>
                <JsonEditor value={settings} onChange={setSettings} />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}