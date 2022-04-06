from cgi import print_directory
from django.http import HttpResponse, JsonResponse
import requests as python_requests
import json
from google.oauth2 import id_token
from google.auth.transport import requests


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request()
            )

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return "The token is either invalid or has expired"


# Create your views here.
def google_authentication(request):
    code = request.GET.get('code')
    CLIENT_ID = "394636177476-a58g5v78eok9lbuifo6pk0t8bicgs84d.apps.googleusercontent.com"
    result = python_requests.post(
        'https://oauth2.googleapis.com/token',
        json={
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': "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",
            'redirect_uri': 'http://127.0.0.1:8000/api/social/google/',
        },
    )
    data_text = json.loads(result.text)
    if data_text.get('error'):
        return JsonResponse(
            {"there was an error": data_text.get('error')},
            status=result.status_code,
        )
    print(data_text)
    token = data_text.get('access_token')
    print(token)

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID
        )

        print(idinfo)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        return HttpResponse(idinfo)
    except ValueError:
        # Invalid token
        pass
