import os
from django.http import HttpResponseRedirect
from httplib2 import Http
import json
import urllib
from social_auth.email_login_or_register import login_or_register


def google_login(request):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
    redirect_uri = os.getenv('SOCIAL_AUTH_GOOGLE_REDIRECT_URI')
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri=token_request_uri,
        response_type=response_type,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
    )
    return HttpResponseRedirect(url)


def google_authenticate(request):
    print(next)
    parser = Http()
    login_failed_url = '/'
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect(
            '{loginfailed}'.format(loginfailed=login_failed_url)
        )

    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = os.getenv('SOCIAL_AUTH_GOOGLE_REDIRECT_URI')
    params = urllib.parse.urlencode(
        {
            'code': request.GET['code'],
            'redirect_uri': redirect_uri,
            'client_id': os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_SECRET'),
            'grant_type': 'authorization_code',
        }
    )
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    resp, content = parser.request(
        access_token_uri, method='POST', body=params, headers=headers
    )
    token_data = json.loads(content)
    resp, content = parser.request(
        "https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(
            accessToken=token_data['access_token']
        )
    )
    google_profile = json.loads(content)

    user_id, res = login_or_register(google_profile)
    response = HttpResponseRedirect('http://127.0.0.1:8080/')
    print(res)
    response.set_cookie('VueBlog', res.get('access'))
    response.set_cookie('VueBlogRefresh', res.get('refresh'))
    response.set_cookie('UserId', user_id)

    return response
