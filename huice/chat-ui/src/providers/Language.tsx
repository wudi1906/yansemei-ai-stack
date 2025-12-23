/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 * 
 * Language Provider for Chat UI internationalization
 */

"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { 
  Language, 
  Translations, 
  getStoredLanguage, 
  setStoredLanguage, 
  getTranslations 
} from '@/lib/i18n';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
  toggleLanguage: () => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>('zh');
  const [translations, setTranslations] = useState<Translations>(getTranslations('zh'));

  useEffect(() => {
    const stored = getStoredLanguage();
    setLanguageState(stored);
    setTranslations(getTranslations(stored));
  }, []);

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang);
    setStoredLanguage(lang);
    setTranslations(getTranslations(lang));
  }, []);

  const toggleLanguage = useCallback(() => {
    const newLang = language === 'zh' ? 'en' : 'zh';
    setLanguage(newLang);
  }, [language, setLanguage]);

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t: translations, toggleLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
