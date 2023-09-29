import React from 'react';
import { clsx } from 'clsx';
import { Outlet } from 'react-router-dom';

import { useApp } from '@/contexts/app';
import { useTheme } from '@/contexts/theme';

import { GoTopButton } from './go_top_button';
import { SidebarToggler } from './sidebar_toggler';
import { Sidebar } from './sidebar';
import { Header } from './header';
import { Footer } from './footer';
import { Loader } from './Loader';

export function Layout() {
    const theme = useTheme();
    const { loading } = useApp();

    return (
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
            <Loader show={loading} />
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
                    <Footer />
                </div>
            </div>
        </div>
    );
}
