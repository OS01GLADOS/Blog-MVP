from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from httplib2 import Http
import json
import urllib
from social_auth.email_login_or_register import login_or_register


def google_login(request):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = '394636177476-a58g5v78eok9lbuifo6pk0t8bicgs84d.apps.googleusercontent.com'
    redirect_uri = "http://127.0.0.1:8000/api/social/google/"
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
    parser = Http()
    login_failed_url = '/'
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect(
            '{loginfailed}'.format(loginfailed=login_failed_url)
        )

    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = "http://127.0.0.1:8000/api/social/google/"
    params = urllib.parse.urlencode(
        {
            'code': request.GET['code'],
            'redirect_uri': redirect_uri,
            'client_id': '394636177476-a58g5v78eok9lbuifo6pk0t8bicgs84d.apps.googleusercontent.com',
            'client_secret': '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',
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
    # this gets the google profile!!
    google_profile = json.loads(content)

    # log the user in
    res = login_or_register(google_profile)

    return JsonResponse(res)
