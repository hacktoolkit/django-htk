# HTK Imports
from htk.api.auth import HTTPBearerAuth
from htk.lib.indeed.api.base import IndeedBaseSyncAPI
from htk.lib.indeed.constants import INDEED_GRAPHQL_API_URL


class IndeedJobSyncAPI(IndeedBaseSyncAPI):
    """API to CREATE/UPDATE/DELETE jobs in Indeed

    Indeed uses GraphQL API to manage job postings
    Ref: https://docs.indeed.com/job-sync-api/
    """

    def upsert(self, payload):
        mutation = """mutation CreateSourcedJobPostings($input: CreateSourcedJobPostingsInput) {
            jobsIngest {
                createSourcedJobPostings(input: $input) {
                    results {
                        jobPosting {
                            sourcedPostingId
                        }
                    }
                }
            }
        }
        """

        variables = {'input': {'jobPostings': [payload]}}
        access_token = self.get_access_token()
        auth = HTTPBearerAuth(access_token)

        response_json, status_code = self.request_post(
            INDEED_GRAPHQL_API_URL,
            auth=auth,
            json={'query': mutation, 'variables': variables},
        )

        return response_json, status_code

    def expire(self, payload):
        mutation = """mutation ExpireSourcedJobsBySourcedPostingId($input: ExpireSourcedJobsBySourcedPostingIdInput!) {
            jobsIngest {
                expireSourcedJobsBySourcedPostingId(input: $input) {
                    results {
                        trackingKey
                        inputData {
                            ... on ExpireSourcedJobBySourcedPostingIdInfo {
                                sourcedPostingId
                            }
                        }
                    }
                }
            }
        }
        """

        variables = {'input': {'jobs': payload}}
        access_token = self.get_access_token()
        auth = HTTPBearerAuth(access_token)

        response_json, status_code = self.request_post(
            INDEED_GRAPHQL_API_URL,
            auth=auth,
            json={'query': mutation, 'variables': variables},
        )

        return response_json, status_code
