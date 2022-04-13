from unittest.mock import patch
from api.views import get_upload_url, createUploadLink
import re
from django.http import HttpRequest


def test_get_upload_url():
    res = get_upload_url('dump_file')
    regex = re.compile(r'.*.s3.amazonaws.com/dump_file')
    assert regex.match(res)


def test_create_upload_link():
    with patch('api.views.get_upload_url') as mock_link:
        mock_link.return_value = {'test': "yes"}
        mock_request = HttpRequest()
        mock_request.GET['filename'] = 'testnameOftile'
        res = createUploadLink(mock_request)
        mock_link.assert_called_with('testnameOftile')
