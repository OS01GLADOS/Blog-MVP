from mixer.backend.django import mixer
from django.contrib.auth.models import User
from .email_login_or_register import login_or_register

import pytest


@pytest.mark.django_db
def test_login_or_register_new_user_creation():
    email = 'testEmail@gmail.com'
    name = 'testName'
    res = login_or_register({"email": email, 'name': name})
    assert User.objects.filter(email=email).first()
