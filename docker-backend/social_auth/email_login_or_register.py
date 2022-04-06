from api.models import Profile
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken


def login_or_register(google_user):
    user = Profile.objects.filter(user__email=google_user.get('email')).first()
    user_id = 0
    if user:
        user_id = user.user.id
        print(user)
        refresh = RefreshToken.for_user(user.user)
    else:
        new_user = User()
        new_user.username = google_user.get('name')
        new_user.email = google_user.get('email')
        new_user.set_password(google_user.get('id'))
        new_user.save()
        new_user.refresh_from_db()
        print(new_user.id)
        user_id = new_user.id
        refresh = RefreshToken.for_user(new_user.user)
    return user_id, {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
