import { Icon } from '@/components/ui/icon';
import { useTheme } from '@/contexts/theme';
import { Link } from 'react-router-dom';

export function HeaderLogo() {
    const { dispatch } = useTheme();

    const handleClick = () => {
        dispatch({ type: 'sidebar', operation: 'toggle' });
    };

    return (
        <div className="horizontal-logo flex lg:hidden justify-between items-center ltr:mr-2 rtl:ml-2">
            <Link to="/" className="main-logo flex items-center shrink-0">
                <button
                    type="button"
                    className="collapse-icon flex-none dark:text-[#d0d2d6] hover:text-primary dark:hover:text-primary flex lg:hidden ltr:ml-2 rtl:mr-2 p-2 rounded-full bg-white-light/40 dark:bg-dark/40 hover:bg-white-light/90 dark:hover:bg-dark/60"
                    onClick={handleClick}
                >
                    <Icon name="double-caret-right" size="md" />
                </button>
                {/* <img src="" alt="" className="w-8 ltr:-ml-1 rtl:-mr-1 inline" /> */}
                <span className="text-2xl ltr:ml-1.5 rtl:mr-1.5 font-semibold align-middle hidden md:inline dark:text-white-light transition-all duration-300">
                    AdminTools
                </span>
            </Link>
        </div>
    );
}
