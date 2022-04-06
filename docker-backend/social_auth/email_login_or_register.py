from api.models import Profile
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken


def login_or_register(google_user):
    user = Profile.objects.filter(user__email=google_user.get('email')).first()
    if user:
        refresh = RefreshToken.for_user(user)
    else:
        new_user = User()
        new_user.username = google_user.get('name')
        new_user.email = google_user.get('email')
        new_user.set_password(google_user.get('id'))
        new_user.save()
        refresh = RefreshToken.for_user(new_user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
