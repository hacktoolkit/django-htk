import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

import { ThemeConfig } from '@/theme_config';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

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
