import React from 'react';

type Action = { type: 'finishLoading' };

interface AppState {
    loading: boolean;
}

export function appReducer(state: AppState, action: Action): AppState {
    switch (action.type) {
        case 'finishLoading':
            return { ...state, loading: false };
    }
}

export const AppContext = React.createContext<
    AppState & { dispatch: React.Dispatch<Action> }
>({
    loading: true,
    dispatch: () => {},
});

export function useApp() {
    const context = React.useContext(AppContext);
    return context;
}
