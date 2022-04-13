import pytest
from api.views import PostViewSet
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from api.models import Post
from api.unit_tests.views_tests.dump_request import Dump_request


@pytest.mark.django_db
def test_post_without_params():
    user = mixer.blend(User)
    user2 = mixer.blend(User)
    post1 = mixer.blend(Post, author=user)
    post2 = mixer.blend(Post, author=user)
    post3 = mixer.blend(Post, author=user2)
    dict_query = {'': ''}
    PostView = PostViewSet(
        request=Dump_request(query=dict_query, user_in=user)
    )
    res = PostView.get_queryset()
    assert len(res) == 3
    assert res.first() == post3
    assert res.last() == post1


@pytest.mark.django_db
def test_post_with_params():
    user = mixer.blend(User)
    user2 = mixer.blend(User)
    post1 = mixer.blend(Post, author=user)
    post2 = mixer.blend(Post, author=user)
    post3 = mixer.blend(Post, author=user2)
    dict_query = {'author': user.username}
    PostView = PostViewSet(
        request=Dump_request(query=dict_query, user_in=user)
    )
    res = PostView.get_queryset()
    assert len(res) == 2
    assert res.first() == post2
    assert res.last() == post1
