import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { Toaster } from 'sonner';

import { Layout } from '@/components/ui/layout';
import DashboardRoute from '@/routes/dashboard';
import { defaultThemeConfig } from '@/theme_config';
import { Error404, Error500 } from '@/components/ui/errors';
import { ThemeContext, themeReducer } from '@/contexts/theme';

const router = createBrowserRouter(
    [
        {
            path: '',
            element: <Layout />,
            children: [
                {
                    index: true,
                    element: <DashboardRoute />,
                },
            ],
        },
        {
            path: '*',
            element: <Error404 />,
        },
    ],
    { basename: '/admintools' },
);

export function AdminToolsApp() {
    const [theme, dispatch] = React.useReducer(
        themeReducer,
        defaultThemeConfig,
    );

    const context = React.useMemo(() => ({ ...theme, dispatch }), [theme]);
    return (
        <ThemeContext.Provider value={context}>
            <ErrorBoundary fallback={<Error500 />}>
                <RouterProvider router={router} />
            </ErrorBoundary>
            <Toaster position="bottom-right" richColors />
        </ThemeContext.Provider>
    );
}
