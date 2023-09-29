import clsx from 'clsx';
import { useTheme } from '@/contexts/theme';
import { SidebarHeader } from './header';
import { NavItem } from '@/components/ui/layout/sidebar/nav_item';

export function Sidebar() {
    const { semiDark } = useTheme();

    return (
        <div className={clsx({ dark: semiDark })}>
            <nav
                className={clsx(
                    'sidebar fixed bottom-0 top-0 h-full min-h-screen',
                    'shadow-sidebar z-50 bg-white transition-all duration-300',
                    'w-[260px] dark:bg-black dark:text-white-dark',
                )}
            >
                <SidebarHeader />
                <ul className="relative space-y-0.5 p-4 py-0 font-semibold">
                    <NavItem to="/" icon="dashboard">
                        Dashboard
                    </NavItem>
                    <NavItem to="/" icon="logout" anchor>
                        Go Back To Site
                    </NavItem>
                </ul>
            </nav>
        </div>
    );
}
