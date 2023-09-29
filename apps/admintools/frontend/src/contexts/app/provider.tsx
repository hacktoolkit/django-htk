import React from 'react';
import { AppContext, appReducer } from './index';

export function AppProvider({ children }: { children: React.ReactNode }) {
    const [app, dispatch] = React.useReducer(appReducer, {
        loading: true,
        paths: [],
    });

    const context = React.useMemo(() => ({ ...app, dispatch }), [app]);

    return (
        <AppContext.Provider value={context}>{children}</AppContext.Provider>
    );
}
