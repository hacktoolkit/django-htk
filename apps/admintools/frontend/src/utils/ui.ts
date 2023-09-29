import { ThemeConfig } from '@/theme_config';

export function applyTheme(theme: ThemeConfig['theme']) {
    let isDarkMode = false;
    if (theme === 'system') {
        isDarkMode =
            window.matchMedia &&
            window.matchMedia('(prefers-color-scheme: dark)').matches;
    } else {
        isDarkMode = theme === 'dark';
    }

    document.querySelector('body')!.classList.toggle('dark', isDarkMode);

    return { theme, isDarkMode };
}
