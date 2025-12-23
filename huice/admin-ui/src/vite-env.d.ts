/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZjVlZZYXc9PTo3YjljMzZhOQ==

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_PROXY: string
  readonly VITE_API_ENDPOINTS: string
  readonly VITE_BACKEND_URL: string
}
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZjVlZZYXc9PTo3YjljMzZhOQ==

interface ImportMeta {
  readonly env: ImportMetaEnv
}