import React from 'react';

import { defaultThemeConfig } from '@/theme_config';

import { ThemeContext, themeReducer } from './index';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
    const [theme, dispatch] = React.useReducer(
        themeReducer,
        defaultThemeConfig,
    );

    const context = React.useMemo(() => ({ ...theme, dispatch }), [theme]);

    return (
        <ThemeContext.Provider value={context}>
            {children}
        </ThemeContext.Provider>
    );
}
