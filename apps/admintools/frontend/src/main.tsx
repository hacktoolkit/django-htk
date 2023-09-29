import 'vite/modulepreload-polyfill';

import React from 'react';
import ReactDOM from 'react-dom/client';

import '@/styles/tailwind.css';

import { AdminToolsApp } from './App';
import { AppProvider } from '@/contexts/app/provider';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <AppProvider>
            <AdminToolsApp />
        </AppProvider>
    </React.StrictMode>,
);
