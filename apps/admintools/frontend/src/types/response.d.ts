import { IconName } from '@/components/ui/icon';

interface BaseAPIResponse {
    status: string;
    success: boolean;
}

type BasePath = {
    url: string;
    label: string;
    icon: IconName;
    show_in_menu: boolean;
};

export type ParentPath = BasePath & {
    children: Path[];
};

export type PagePath = BasePath & {
    api_url: string;
    index: boolean;
};

export type Path = ParentPath | PagePath;

export interface AppResponse extends BaseAPIResponse {
    paths: Path[];
}
