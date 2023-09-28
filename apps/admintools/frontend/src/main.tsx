import 'vite/modulepreload-polyfill';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { AdminToolsApp } from './App';

import './tailwind.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <AdminToolsApp />
    </React.StrictMode>,
);
