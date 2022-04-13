from social_auth.views import (
    google_authenticate,
    google_login,
    token_google_login,
    token_google_authenticate,
    google_send_authenticate_request,
)
from unittest.mock import MagicMock, patch
import json
from django.http import HttpRequest


def test_google_login():
    res = google_login('')
    assert res.status_code == 302
    url = 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=google_id&redirect_uri=uri&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email'
    assert res.url == url


def test_token_google_login():
    res = token_google_login('')
    assert res.status_code == 302
    url = 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=google_id&redirect_uri=uri_token&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email'
    assert res.url == url


def test_google_authenticate():
    with patch(
        'social_auth.views.google_send_authenticate_request'
    ) as mock_authenticate_request:
        mock_authenticate_request.return_value = 983, {
            'access': 'token1',
            'refresh': 'token2',
        }
        res = google_authenticate('')
        assert str(res.cookies.get('VueBlog').value) == 'token1'
        assert str(res.cookies.get('VueBlogRefresh').value) == 'token2'
        assert str(res.cookies.get('UserId').value) == '983'


def test_token_google_authenticate():
    with patch(
        'social_auth.views.google_send_authenticate_request'
    ) as mock_authenticate_request:
        mock_authenticate_request.return_value = 983, {
            'access': 'token1',
            'refresh': 'token2',
        }
        res = token_google_authenticate('')
        res = json.loads(res.content)
        assert res.get('access') == 'token1'
        assert res.get('refresh') == 'token2'


class CustomHttp:
    def request(access_token_uri, method='get', body='none', headers='none'):
        return 1, '{"access_token": "example_token"}'


def test_google_send_authenticate_request():
    with patch('social_auth.views.Http') as mock_http:
        with patch('social_auth.views.login_or_register') as result_mock:
            mock_request = HttpRequest()
            mock_request.GET['code'] = 'sample_code'
            mock_http.return_value = CustomHttp

            res = google_send_authenticate_request(mock_request, '')

            result_mock.assert_called_with({'access_token': 'example_token'})


def test_google_send_authenticate_request_authenticated_error():
    mock_request = HttpRequest()
    res = google_send_authenticate_request(mock_request, '')
    assert res.status_code == 401
