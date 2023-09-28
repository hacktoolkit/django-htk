import { NavLink } from 'react-router-dom';
import { Icon } from '@/components/ui/icon';
import { useTheme } from '@/contexts/theme';

export function SidebarHeader() {
    const { dispatch } = useTheme();
    const handleToggleSidebar = () => {
        dispatch({ type: 'sidebar', operation: 'toggle' });
    };
    return (
        <div className="flex justify-between items-center px-4 py-3">
            <NavLink to="/" className="main-logo flex items-center shrink-0">
                {/* <img src="" alt="" className="w-8 ml-[5px] flex-none" /> */}
                <span className="text-2xl ltr:ml-1.5 rtl:mr-1.5 font-semibold align-middle lg:inline dark:text-white-light">
                    AdminTools
                </span>
            </NavLink>
            <button
                type="button"
                className="collapse-icon w-8 h-8 rounded-full flex items-center hover:bg-gray-500/10 dark:hover:bg-dark-light/10 dark:text-white-light transition duration-300 rtl:rotate-180"
                onClick={handleToggleSidebar}
            >
                <Icon name="double-caret-left" size="md" className="m-auto" />
            </button>
        </div>
    );
}
