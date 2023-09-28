import { useTheme } from '@/contexts/theme';
import clsx from 'clsx';

export function SidebarToggler() {
    const { isSidebarOpen: sidebarOpen, dispatch } = useTheme();

    const handleClick = () => {
        dispatch({ type: 'sidebar', operation: 'toggle' });
    };

    return (
        <div
            className={clsx('fixed inset-0 bg-[black]/60 z-50 lg:hidden', {
                hidden: !sidebarOpen,
            })}
            onClick={handleClick}
        />
    );
}
