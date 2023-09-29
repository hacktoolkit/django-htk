import { Outlet, RouteObject, createBrowserRouter } from 'react-router-dom';

import { Error404 } from '@/components/ui/errors';
import { Layout } from '@/components/ui/layout';

import DashboardRoute from './dashboard';
import { ParentPath, Path } from '@/types/response';
import { DynamicRoute } from '@/routes/dynamic_route';

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

export function isParentPath(path: Path): path is ParentPath {
    return 'children' in (path as ParentPath);
}

export function build_paths(paths: Path[]): RouteObject[] {
    return paths.map((path) =>
        isParentPath(path)
            ? {
                  path: path.url,
                  element: <Outlet />,
                  children: build_paths(path.children),
              }
            : {
                  path: path.index ? '' : path.url,
                  index: path.index ?? undefined,
                  element: <DynamicRoute />,
              },
    );
}

export function buildRoutes(paths: Path[]) {
    // TODO: build this array from backend data
    const appRoutes: RouteObject[] = [dashboardRoute, ...build_paths(paths)];

    const router = createBrowserRouter(
        [{ ...baseRoute, children: appRoutes } as RouteObject, notFoundRoute],
        {
            basename: '/admintools',
        },
    );

    return router;
}
