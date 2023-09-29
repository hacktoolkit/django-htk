import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { RouterProvider } from 'react-router-dom';
import { Toaster } from 'sonner';

import { Error500 } from '@/components/ui/errors';
import { ThemeProvider } from '@/contexts/theme';
import { buildRoutes } from '@/routes';
import { useFetchApp } from '@/hooks/api/useFetchApp';
import { useApp } from '@/contexts/app';

export function AdminToolsApp() {
    const { dispatch } = useApp();
    const { data, isLoading } = useFetchApp();

    const router = buildRoutes();

    React.useEffect(() => {
        if (!isLoading) {
            dispatch({ type: 'finishLoading' });
        }
    }, [isLoading, dispatch]);

    React.useEffect(() => {
        if (typeof data !== 'undefined') {
            dispatch({ type: 'setPaths', paths: data.paths });
        }
    }, [data, dispatch]);

    return (
        <ThemeProvider>
            <ErrorBoundary fallback={<Error500 />}>
                <RouterProvider router={router} />
            </ErrorBoundary>
            <Toaster position="bottom-right" richColors />
        </ThemeProvider>
    );
}
