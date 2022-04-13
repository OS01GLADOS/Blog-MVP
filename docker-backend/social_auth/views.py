import os
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect
from httplib2 import Http
import json
import urllib
from social_auth.email_login_or_register import login_or_register


def return_uri(redirect_url):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri=token_request_uri,
        response_type=response_type,
        client_id=client_id,
        redirect_uri=redirect_url,
        scope=scope,
    )
    return url


def google_login(request):
    url = return_uri(os.getenv('SOCIAL_AUTH_GOOGLE_REDIRECT_URI'))
    return HttpResponseRedirect(url)


def token_google_login(request):
    url = return_uri(os.getenv('SOCIAL_AUTH_GOOGLE_REDIRECT_URI_TOKEN'))
    return HttpResponseRedirect(url)


def google_send_authenticate_request(request, redirect_uri):
    parser = Http()
    login_failed_url = '/'
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponse('Unauthorized', status=401)

    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
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
    return login_or_register(google_profile)


def google_authenticate(request):
    redirect_uri = os.getenv('SOCIAL_AUTH_GOOGLE_REDIRECT_URI')
    user_id, res = google_send_authenticate_request(request, redirect_uri)
    response = HttpResponseRedirect('http://127.0.0.1:8080/')
    response.set_cookie('VueBlog', res.get('access'))
    response.set_cookie('VueBlogRefresh', res.get('refresh'))
    response.set_cookie('UserId', user_id)
    return response


def token_google_authenticate(request):
    redirect_uri = os.getenv('SOCIAL_AUTH_GOOGLE_REDIRECT_URI_TOKEN')
    user_id, res = google_send_authenticate_request(request, redirect_uri)
    return JsonResponse(res)
