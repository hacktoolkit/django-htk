import StaticAxios, { AxiosResponse, CreateAxiosDefaults } from 'axios';
import { toast } from 'sonner';

export const defaultConfig: CreateAxiosDefaults = {
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    responseType: 'json',
};

export const axios = StaticAxios.create({ ...defaultConfig });

axios.interceptors.request.use((request) => {
    document.querySelector('body')?.classList.add('fetch-loading');
    return request;
});

axios.interceptors.response.use(
    (response: AxiosResponse): AxiosResponse => {
        document.querySelector('body')?.classList.remove('fetch-loading');
        return response;
    },
    <T>(error: T): Promise<T> => {
        toast.error(`An error occurred while fetching data: ${error}`);
        return Promise.reject(error);
    },
);

export const fetcher = (url: string) =>
    axios.get(url).then((response) => response.data);
