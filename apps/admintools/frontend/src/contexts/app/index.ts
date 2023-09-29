import { Path } from '@/types/response';
import React from 'react';

type Action = { type: 'finishLoading' } | { type: 'setPaths'; paths: Path[] };

interface AppState {
    loading: boolean;
    paths: Path[];
}

export function appReducer(state: AppState, action: Action): AppState {
    switch (action.type) {
        case 'finishLoading':
            return { ...state, loading: false };
        case 'setPaths':
            return { ...state, loading: false, paths: action.paths };
        default:
            return state;
    }
}

export const AppContext = React.createContext<
    AppState & { dispatch: React.Dispatch<Action> }
>({
    loading: true,
    paths: [],
    dispatch: () => {},
});

export function useApp() {
    const context = React.useContext(AppContext);
    return context;
}
