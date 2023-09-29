interface BaseAPIResponse {
    status: string;
    success: boolean;
}

export interface AppResponse extends BaseAPIResponse {
    user_menu: string[];
}
