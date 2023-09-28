import { ThemeConfig, defaultThemeConfig } from '@/theme_config';
import { applyTheme } from '@/utils/ui';
import React from 'react';

type Action =
    | { type: 'theme'; theme: ThemeConfig['theme'] }
    | { type: 'menu'; menu: ThemeConfig['menu'] }
    | { type: 'sidebar'; operation: 'open' | 'close' | 'toggle' };

export function themeReducer(state: ThemeConfig, action: Action): ThemeConfig {
    switch (action.type) {
        case 'theme':
            return { ...state, theme: applyTheme(action.theme) };
        case 'menu':
            return { ...state, menu: action.menu };
        case 'sidebar':
            return {
                ...state,
                isSidebarOpen:
                    action.operation === 'toggle'
                        ? !state.isSidebarOpen
                        : action.operation === 'open',
            };
        default:
            return state;
    }
}

export const ThemeContext = React.createContext<
    ThemeConfig & { dispatch: React.Dispatch<Action> }
>({
    ...defaultThemeConfig,
    dispatch: () => {},
});

// Custom hook to easily access the ThemeContext
export function useTheme() {
    const theme = React.useContext(ThemeContext);
    return theme;
}
