/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import AppRouter from './AppRouter'
import './i18n.ts';
import 'katex/dist/katex.min.css';
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZWV05sY3c9PToyZjFkNjcwMw==

// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZWV05sY3c9PToyZjFkNjcwMw==


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppRouter />
  </StrictMode>
)