import { RouteObject, createBrowserRouter } from 'react-router-dom';

import { Error404 } from '@/components/ui/errors';
import { Layout } from '@/components/ui/layout';

import DashboardRoute from './dashboard';

const baseRoute: RouteObject = {
    path: '',
    element: <Layout />,
};

const dashboardRoute: RouteObject = {
    index: true,
    element: <DashboardRoute />,
};

const notFoundRoute: RouteObject = {
    path: '*',
    element: <Error404 />,
};

export function buildRoutes() {
    // TODO: build this array from backend data
    const appRoutes: RouteObject[] = [dashboardRoute];

    const router = createBrowserRouter(
        [{ ...baseRoute, children: appRoutes } as RouteObject, notFoundRoute],
        {
            basename: '/admintools',
        },
    );

    return router;
}
