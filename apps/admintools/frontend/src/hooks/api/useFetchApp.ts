import { AppResponse } from '@/types/response';
import { fetcher } from '@/utils/axios';
import useSWR from 'swr';

export function useFetchApp() {
    const value = useSWR<AppResponse>(APP_CONFIG_URL, fetcher);
    return value;
}
