import React from 'react';
import { clsx } from 'clsx';
import { Outlet } from 'react-router-dom';
import { ThemeContext, themeReducer } from '@/contexts/theme';
import { ThemeConfig } from '@/theme_config';
import { GoTopButton } from './go_top_button';
import { SidebarToggler } from './sidebar_toggler';
import { Sidebar } from './sidebar';
import { Header } from './header';

export function Layout({ themeConfig }: { themeConfig: ThemeConfig }) {
    const [theme, dispatch] = React.useReducer(themeReducer, themeConfig);

    const context = React.useMemo(() => ({ ...theme, dispatch }), [theme]);

    return (
        <ThemeContext.Provider value={context}>
            <div
                className={clsx(
                    'main-section antialiased relative font-nunito, text-sm font-normal',
                    theme.menu,
                    theme.layout,
                    theme.rtlClass,
                    {
                        'toggle-sidebar': !theme.isSidebarOpen,
                    },
                )}
            >
                <SidebarToggler />
                <GoTopButton />
                <div
                    className={clsx(
                        theme.navbar,
                        'main-container text-black dark:text-white-dark min-h-screen',
                    )}
                >
                    <Sidebar />
                    <div className="main-content flex flex-col min-h-screen">
                        <Header />
                        <React.Suspense>
                            <div
                                className={clsx(
                                    theme.animation,
                                    'p-6 animate__animated',
                                )}
                            >
                                <Outlet />
                            </div>
                        </React.Suspense>
                    </div>
                </div>
            </div>
        </ThemeContext.Provider>
    );
}
