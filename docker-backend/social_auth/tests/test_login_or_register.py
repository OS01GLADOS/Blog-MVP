from mixer.backend.django import mixer
from django.contrib.auth.models import User
from social_auth.email_login_or_register import login_or_register
from unittest.mock import patch

import pytest


class Result:
    def __init__(self, refresh, access_token):
        self.refresh = refresh
        self.access_token = access_token

    def __str__(self):
        return str(self.refresh)


@pytest.mark.django_db
def test_login_or_register_existing_user():
    with patch(
        "social_auth.email_login_or_register.RefreshToken.for_user"
    ) as refresh_token_mock:
        user = mixer.blend(User)
        refresh_token_mock.return_value = Result(user.id, user.id)
        user_id, res = login_or_register(
            {"email": user.email, 'name': user.username}
        )
        assert res == {'refresh': str(user.id), 'access': str(user.id)}


@pytest.mark.django_db
def test_login_or_register_new_user():
    with patch(
        "social_auth.email_login_or_register.RefreshToken.for_user"
    ) as refresh_token_mock:
        refresh_token_mock.return_value = Result('name', 'name')
        user_id, res = login_or_register({"email": 'email', 'name': 'name'})
        user = User.objects.filter(id=user_id, username='name').first()
        assert user
        assert res == {'refresh': 'name', 'access': 'name'}
