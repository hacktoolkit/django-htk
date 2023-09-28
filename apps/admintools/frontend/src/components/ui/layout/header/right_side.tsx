import { ThemeSwitcher } from './theme_switcher';

export function HeaderRightSide() {
    return (
        <div className="sm:flex-1 ltr:sm:ml-0 ltr:ml-auto sm:rtl:mr-0 rtl:mr-auto flex items-center space-x-1.5 lg:space-x-2 rtl:space-x-reverse dark:text-[#d0d2d6]">
            <div className="sm:ltr:mr-auto sm:rtl:ml-auto"></div>
            <ThemeSwitcher />
        </div>
    );
}
