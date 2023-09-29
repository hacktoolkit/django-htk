interface BaseAPIResponse {
    status: string;
    success: boolean;
}

type Path =
    | {
          index: true;
          api_url: string;
      }
    | {
          url: string;
          api_url: string;
          label: string;
          icon: string;
          children?: Path[];
      };

export interface AppResponse extends BaseAPIResponse {
    paths: Path[];
}
