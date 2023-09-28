import { Layout } from '@/components/ui/layout';
import DashboardRoute from '@/routes/dashboard';
import { defaultThemeConfig } from '@/theme_config';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

const router = createBrowserRouter(
    [
        {
            path: '',
            element: <Layout themeConfig={defaultThemeConfig} />,
            children: [
                {
                    index: true,
                    element: <DashboardRoute />,
                },
            ],
        },
    ],
    { basename: '/admintools' },
);

export function AdminToolsApp() {
    return <RouterProvider router={router} />;
}
