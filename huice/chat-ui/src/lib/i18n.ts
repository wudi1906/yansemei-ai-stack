/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 * 
 * Internationalization (i18n) support for Chat UI
 */

export type Language = 'zh' | 'en';

export interface Translations {
  // Common
  loading: string;
  cancel: string;
  send: string;
  scrollToBottom: string;
  newChat: string;
  
  // Chat input
  inputPlaceholder: string;
  hideToolCalls: string;
  uploadPdfOrImage: string;
  
  // Messages
  thinking: string;
  regenerate: string;
  copy: string;
  copied: string;
  copyFailed: string;
  
  // History
  chatHistory: string;
  noHistory: string;
  deleteChat: string;
  confirmDelete: string;
  
  // Errors
  errorOccurred: string;
  tryAgain: string;
  
  // File upload
  fileUploading: string;
  fileUploaded: string;
  fileUploadFailed: string;
  unsupportedFileType: string;
  
  // Language toggle
  switchToEnglish: string;
  switchToChinese: string;
  
  // App title
  appTitle: string;
  enterprisePlatform: string;
}

const translations: Record<Language, Translations> = {
  zh: {
    loading: '加载中...',
    cancel: '取消',
    send: '发送',
    scrollToBottom: '滚动到底部',
    newChat: '新对话',
    inputPlaceholder: '请输入您的消息...',
    hideToolCalls: '隐藏工具调用',
    uploadPdfOrImage: '上传PDF或图片',
    thinking: '思考中...',
    regenerate: '重新生成',
    copy: '复制',
    copied: '已复制',
    copyFailed: '复制失败',
    chatHistory: '对话历史',
    noHistory: '暂无对话历史',
    deleteChat: '删除对话',
    confirmDelete: '确定要删除这个对话吗？此操作无法撤销。',
    errorOccurred: '发生错误，请重试。',
    tryAgain: '重试',
    fileUploading: '文件上传中...',
    fileUploaded: '文件上传成功',
    fileUploadFailed: '文件上传失败',
    unsupportedFileType: '不支持的文件类型',
    switchToEnglish: 'Switch to English',
    switchToChinese: '切换到中文',
    appTitle: 'AuroraAI',
    enterprisePlatform: '企业级智能平台',
  },
  en: {
    loading: 'Loading...',
    cancel: 'Cancel',
    send: 'Send',
    scrollToBottom: 'Scroll to bottom',
    newChat: 'New Chat',
    inputPlaceholder: 'Type your message...',
    hideToolCalls: 'Hide tool calls',
    uploadPdfOrImage: 'Upload PDF or Image',
    thinking: 'Thinking...',
    regenerate: 'Regenerate',
    copy: 'Copy',
    copied: 'Copied',
    copyFailed: 'Copy failed',
    chatHistory: 'Chat History',
    noHistory: 'No chat history',
    deleteChat: 'Delete Chat',
    confirmDelete: 'Are you sure you want to delete this chat? This action cannot be undone.',
    errorOccurred: 'An error occurred. Please try again.',
    tryAgain: 'Try again',
    fileUploading: 'Uploading file...',
    fileUploaded: 'File uploaded successfully',
    fileUploadFailed: 'File upload failed',
    unsupportedFileType: 'Unsupported file type',
    switchToEnglish: 'Switch to English',
    switchToChinese: '切换到中文',
    appTitle: 'AuroraAI',
    enterprisePlatform: 'Enterprise AI Platform',
  },
};

const STORAGE_KEY = 'chat-ui-language';

export function getStoredLanguage(): Language {
  if (typeof window === 'undefined') return 'zh';
  const stored = localStorage.getItem(STORAGE_KEY);
  return (stored === 'en' || stored === 'zh') ? stored : 'zh';
}

export function setStoredLanguage(lang: Language): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, lang);
}

export function getTranslations(lang: Language): Translations {
  return translations[lang];
}

export function t(key: keyof Translations, lang?: Language): string {
  const currentLang = lang || getStoredLanguage();
  return translations[currentLang][key];
}
