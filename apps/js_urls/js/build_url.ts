import _ from 'lodash';

// It must be defined as global or external in webpack
import { urls } from 'site';

export function buildUrl(urlName: string, args: (string|number)[] = []): string {
    const baseUrl = urls[urlName];
    let url = baseUrl;
    if (args) {
        const parts = baseUrl.split('{0}');
        const pairs = _.zip(parts, args);
        url = _.flatMap(pairs, (pair) => pair.join('')).join('');
    }
    return url;
}
