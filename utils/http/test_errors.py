# Third Party (PyPI) Imports
import pytest

# HTK Imports
from htk.api.utils import json_response_error
from htk.utils.http.errors import HttpErrorResponseError


@pytest.mark.parametrize(
    'response,status_code',
    [
        ['Not Found', 404],
        [json_response_error({'message': 'Not Found'}, status=404), 404],
        [json_response_error({'message': 'Not Found'}, status=400), 400],
    ],
)
def test_http_error_response_error_exception(response, status_code):
    try:
        raise HttpErrorResponseError(response)
    except HttpErrorResponseError as e:
        assert 'Not Found' in str(e.response.content)
        assert e.response.status_code == status_code
    except Exception as e:
        pytest.fail('Unexpected exception: %s' % e)
