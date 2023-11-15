import pytest
from htk.utils.http.errors import HttpErrorResponseError
from htk.api.utils import json_response_error


@pytest.mark.parametrize(
    'response,status_code',
    [
        ['Not Found', 404],
        [{'message': 'Not Found'}, 404],
        [json_response_error({'message': 'Not Found'}, status=404), 404],
    ],
)
def test_http_error_response_error_exception(response, status_code):
    try:
        raise HttpErrorResponseError(response)
    except HttpErrorResponseError as e:
        assert e.response == response
        assert e.response.status_code == 404
    pass
