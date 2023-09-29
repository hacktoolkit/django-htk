import { useTheme } from '@/contexts/theme';
import { ThemeConfig } from '@/theme_config';
import { Laptop2Icon, LucideIcon, MoonIcon, SunIcon } from 'lucide-react';

const iconMap: { [key in ThemeConfig['theme']]: LucideIcon } = {
    light: SunIcon,
    dark: MoonIcon,
    system: Laptop2Icon,
};

const nextThemeMap: { [key in ThemeConfig['theme']]: ThemeConfig['theme'] } = {
    light: 'dark',
    dark: 'system',
    system: 'light',
};

export function ThemeSwitcher() {
    const { theme, dispatch } = useTheme();

    const handleClick = () => {
        dispatch({ type: 'theme', theme: nextThemeMap[theme] });
    };

    const Icon = iconMap[theme];

    return (
        <button
            type="button"
            className="flex items-center p-2 rounded-full bg-white-light/40 dark:bg-dark/40 hover:text-primary hover:bg-white-light/90 dark:hover:bg-dark/60"
            onClick={handleClick}
        >
            <Icon className="w-5 h-5" />
        </button>
    );
}
