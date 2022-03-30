from django.conf import settings
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_login_correct_credentials():
    client = APIClient()
    res = client.login(username='Taro', password="1234")
    assert res
