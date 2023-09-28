import { Icon, IconName } from '@/components/ui/icon';
import { useTheme } from '@/contexts/theme';
import { ThemeConfig } from '@/theme_config';

const iconMap: { [key in ThemeConfig['theme']]: IconName } = {
    light: 'sun',
    dark: 'moon',
    system: 'notebook',
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

    return (
        <button
            type="button"
            className="flex items-center p-2 rounded-full bg-white-light/40 dark:bg-dark/40 hover:text-primary hover:bg-white-light/90 dark:hover:bg-dark/60"
            onClick={handleClick}
        >
            <Icon name={iconMap[theme]} size="md" />
        </button>
    );
}
