import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from api.serializers import ProfileSerializer
from api.models import Profile


@pytest.mark.django_db
def test_profile_serializers_create():
    profileSerializer = ProfileSerializer()
    validated_data = {
        'user': {'username': 'ghijhhjjhl;j', 'email': "gkjhgjhbukhiuhiu"},
        'password': 'vguhhjhbkh',
    }
    res = profileSerializer.create(validated_data=validated_data)
    assert res == User.objects.first().profile
    assert res.user == User.objects.first()


@pytest.mark.django_db
def test_profile_serializers_update():
    profileSerializer = ProfileSerializer()
    user_test = User.objects.create(username='taro', password='1234')
    user_test.save()
    validated_data = {
        'user': {
            'username': 'new_username',
        },
        'image': 'new_image',
        'password': 'test_password',
    }
    res = profileSerializer.update(
        instance=user_test.profile, validated_data=validated_data
    )
    assert res.user == User.objects.first()


@pytest.mark.django_db
def test_profile_no_changes():
    profileSerializer = ProfileSerializer()
    user_test = User.objects.create(username='taro', password='1234')
    user_test.save()
    res = profileSerializer.update(
        instance=user_test.profile, validated_data={}
    )
    assert res.user == User.objects.first()
