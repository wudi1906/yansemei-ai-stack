/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZTV2hVWmc9PTo3NDE5YzM1ZQ==

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZTV2hVWmc9PTo3NDE5YzM1ZQ==

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);