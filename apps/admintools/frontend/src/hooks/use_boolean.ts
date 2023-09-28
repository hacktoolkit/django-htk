import React from 'react';

export function useBoolean(
    initial: boolean = false,
): [
    state: boolean,
    setTrue: () => void,
    setFalse: () => void,
    toggle: () => void,
] {
    const [state, setState] = React.useState<boolean>(initial);

    const setTrue = () => setState(true);
    const setFalse = () => setState(false);
    const toggle = () => setState(!state);

    return [state, setTrue, setFalse, toggle];
}
