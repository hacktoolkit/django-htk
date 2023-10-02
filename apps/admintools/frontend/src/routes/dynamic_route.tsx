import React from 'react';
import useSWR from 'swr';

import { axios, fetcher } from '@/utils/axios';

export function DynamicRoute() {
    const { data } = useSWR('/admintools/pages/users/', (url) =>
        axios.options(url).then((response) => response.data),
    );

    React.useEffect(() => {
        console.log(data);
    }, [data]);

    return <div>Dynamic Route</div>;
}
