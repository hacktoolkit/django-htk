import { Link } from 'react-router-dom';
import { useTheme } from '@/contexts/theme';

import { ErrorBase } from './base';

export function Error503() {
    const { isDarkMode } = useTheme();

    return (
        <ErrorBase>
            <img
                src={
                    isDarkMode
                        ? '/static/admintools/images/503-dark.svg'
                        : '/static/admintools/images/503-light.svg'
                }
                alt="503"
                className="mx-auto w-full max-w-xs object-cover md:max-w-xl"
            />
            <p className="mt-5 text-base dark:text-white">
                Ups! Something went wrong!
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
