/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { defineConfig } from 'vite'
import path from 'path'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'

// RAG Core 后端地址
// Docker 环境使用 rag-core:9621，本地开发使用 127.0.0.1:9621
const BACKEND_URL = process.env.VITE_BACKEND_URL || 'http://rag-core:9621'

// 代理配置
const proxyOptions = {
  target: BACKEND_URL,
  changeOrigin: true,
  secure: false
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  base: '/webui/',
  build: {
    outDir: path.resolve(__dirname, '../lightrag/api/webui'),
    emptyOutDir: true,
    chunkSizeWarningLimit: 3800,
    rollupOptions: {
      output: {
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['chat.yansemei.com'],
    proxy: {
      '/api': {
        ...proxyOptions,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/documents': proxyOptions,
      '/graphs': proxyOptions,
      '/graph': proxyOptions,
      '/health': proxyOptions,
      '/query': proxyOptions,
      '/docs': proxyOptions,
      '/redoc': proxyOptions,
      '/openapi.json': proxyOptions,
      '/login': proxyOptions,
      '/auth-status': proxyOptions,
      '/static': proxyOptions
    }
  }
})
// TODO  MS8yOmFIVnBZMlhsa0xUb3Y2bzZXSGxNYlE9PTpkOTIzMTQ1Nw==