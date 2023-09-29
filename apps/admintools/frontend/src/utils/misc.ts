export function setLocalStorage<T>(items: Partial<T>): Partial<T> {
    (Object.keys(items) as (keyof T)[]).forEach((key) => {
        window.localStorage.setItem(key.toString(), items[key] as string);
    });
    return items;
}

export function getStorageItemOrDefault<T>(name: string, def: T): T {
    const localStorageItem = window.localStorage.getItem(name);
    let result = def;
    if (localStorageItem) {
        if (typeof def === 'boolean') {
            const booleanItem = localStorageItem === 'true';
            result = booleanItem as T;
        } else {
            result = localStorageItem as T;
        }
    }
    return result;
}
