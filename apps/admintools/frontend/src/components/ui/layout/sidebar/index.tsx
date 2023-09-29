import clsx from 'clsx';
import { useTheme } from '@/contexts/theme';
import { SidebarHeader } from './header';
import { NavLink } from 'react-router-dom';
import { Icon } from '@/components/ui/icon';

export function Sidebar() {
    const { semiDark } = useTheme();

    return (
        <div className={clsx({ dark: semiDark })}>
            <nav
                className={clsx(
                    'sidebar fixed min-h-screen h-full top-0 bottom-0',
                    'shadow-sidebar z-50 transition-all duration-300 bg-white',
                    'dark:bg-black dark:text-white-dark w-[260px]',
                )}
            >
                <SidebarHeader />
                <ul className="relative font-semibold space-y-0.5 p-4 py-0">
                    <li className="nav-item">
                        <NavLink to="/" className="group">
                            <div className="flex items-center">
                                <Icon
                                    name="dashboard"
                                    className="group-hover:!text-primary shrink-0"
                                />
                                <span className="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">
                                    Dashboard
                                </span>
                            </div>
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <a href="/" className="group">
                            <div className="flex items-center">
                                <Icon
                                    name="logout"
                                    className="group-hover:!text-primary shrink-0"
                                />
                                <span className="ltr:pl-3 rtl:pr-3 text-black dark:text-[#506690] dark:group-hover:text-white-dark">
                                    Go Back To Site
                                </span>
                            </div>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    );
}
