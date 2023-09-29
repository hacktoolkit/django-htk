import { ThemeConfig, defaultThemeConfig } from '@/theme_config';
import { applyTheme } from '@/utils/ui';
import { setLocalStorage } from '@/utils/misc';
import React from 'react';

export * from './provider';

type Action =
    | { type: 'theme'; theme: ThemeConfig['theme'] }
    | { type: 'menu'; menu: ThemeConfig['menu'] }
    | { type: 'sidebar'; operation: 'open' | 'close' | 'toggle' };

export function themeReducer(state: ThemeConfig, action: Action): ThemeConfig {
    switch (action.type) {
        case 'theme':
            return { ...state, ...setLocalStorage(applyTheme(action.theme)) };
        case 'menu':
            return { ...state, menu: action.menu };
        case 'sidebar':
            return {
                ...state,
                ...setLocalStorage({
                    isSidebarOpen:
                        action.operation === 'toggle'
                            ? !state.isSidebarOpen
                            : action.operation === 'open',
                }),
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
    const context = React.useContext(ThemeContext);
    return context;
}
