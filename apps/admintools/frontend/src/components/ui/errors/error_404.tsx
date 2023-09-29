import { Link } from 'react-router-dom';
import { useTheme } from '@/contexts/theme';

import { ErrorBase } from './base';

export function Error404() {
    const { isDarkMode } = useTheme();

    return (
        <ErrorBase>
            <img
                src={
                    isDarkMode
                        ? '/static/admintools/images/404-dark.svg'
                        : '/static/admintools/images/404-light.svg'
                }
                alt="404"
                className="mx-auto -mt-10 w-full max-w-xs object-cover md:-mt-14 md:max-w-xl"
            />
            <p className="mt-5 text-base dark:text-white">
                The page you requested was not found!
            </p>
            <Link
                to="/"
                className="btn btn-gradient mx-auto !mt-7 w-max border-0 uppercase shadow-none"
            >
                Dashboard
            </Link>
        </ErrorBase>
    );
}
