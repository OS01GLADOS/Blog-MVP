import pytest
from api.views import ProfileViewSet
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from api.unit_tests.views_tests.dump_request import Dump_request


@pytest.mark.django_db
def test_profile_queryset_without_parameters():
    user = mixer.blend(User)
    user2 = mixer.blend(User)
    ProfileView = ProfileViewSet(request=Dump_request(query={}, user_in=user))
    res = ProfileView.get_queryset()
    assert len(res) == 1
    assert res.first() == user.profile


@pytest.mark.django_db
def test_profile_queryset_with_parameters():
    user = mixer.blend(User)
    user2 = mixer.blend(User)
    ProfileView = ProfileViewSet(
        request=Dump_request(query={'self': True}, user_in=user)
    )
    res = ProfileView.get_queryset()
    assert len(res) == 1
    assert res.first() == user.profile


@pytest.mark.django_db
def test_profile_queryset_superuser():
    user = mixer.blend(User, is_superuser=True)
    user2 = mixer.blend(User)
    ProfileView = ProfileViewSet(request=Dump_request(query={}, user_in=user))
    res = ProfileView.get_queryset()
    assert len(res) == 2
    assert res.first() == user.profile
    assert res.last() == user2.profile
