import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { RouterProvider } from 'react-router-dom';
import { Toaster } from 'sonner';

import { Error500 } from '@/components/ui/errors';
import { ThemeProvider } from '@/contexts/theme';
import { buildRoutes } from '@/routes';
import { useFetchApp } from '@/hooks/api/useFetchApp';
import { useApp } from '@/contexts/app';
import { Loader } from '@/components/ui/layout/Loader';

export function AdminToolsApp() {
    const { loading, dispatch } = useApp();
    const { data } = useFetchApp();

    const router = buildRoutes(data?.paths ?? []);

    React.useEffect(() => {
        if (typeof data !== 'undefined') {
            dispatch({ type: 'setPaths', paths: data.paths });
        }
    }, [data, dispatch]);

    return loading ? (
        <Loader show />
    ) : (
        <ThemeProvider>
            <ErrorBoundary fallback={<Error500 />}>
                <RouterProvider router={router} />
            </ErrorBoundary>
            <Toaster position="bottom-right" richColors />
        </ThemeProvider>
    );
}
