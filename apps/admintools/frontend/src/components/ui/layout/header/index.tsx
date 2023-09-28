import { useTheme } from '@/contexts/theme';
import clsx from 'clsx';
import { HeaderLogo } from './logo';
import { HeaderLeftSide } from './left_side';
import { HeaderRightSide } from './right_side';

export function Header() {
    const { semiDark, menu } = useTheme();
    return (
        <header
            className={clsx(
                'z-40 shadow-sm relative bg-white flex w-full items-center px-5 py-2.5 dark:bg-black',
                semiDark && menu === 'horizontal' && 'dark',
            )}
        >
            <HeaderLogo />
            <HeaderLeftSide />
            <HeaderRightSide />
        </header>
    );
}
