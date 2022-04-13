import pytest
from mixer.backend.django import mixer
from api.serializers import PostSerializer
from api.models import PostAudio, Post, PostPicture, Comment
from django.contrib.auth.models import User
from api.unit_tests.views_tests.dump_request import Dump_request


@pytest.mark.django_db
def test_post_serializers_create():
    user = mixer.blend(User)
    post = PostSerializer(context={'request': Dump_request({}, user)})
    validated_data = {
        'title': 'fuiugfufxyuyxyyf',
        'content': 'dsfdhuyhgfyuygygf',
    }
    res = post.create(validated_data=validated_data)
    assert res == Post.objects.all().first()


@pytest.mark.django_db
def test_post_serializers_update():
    user = mixer.blend(User)
    post = mixer.blend(Post)
    postSerializer = PostSerializer(
        context={'request': Dump_request({}, user)}
    )
    validated_data = {
        'title': 'fuiugfufxyuyxyyf',
        'content': 'dsfdhuyhgfyuygygf',
    }
    res = postSerializer.update(post, validated_data=validated_data)
    assert res == Post.objects.all().first()


@pytest.mark.django_db
def test_post_serializers_get_audios():
    post = mixer.blend(Post)
    audio2 = mixer.blend(PostAudio)
    audio1 = mixer.blend(PostAudio, post=post)
    postSerializer = PostSerializer()
    res = postSerializer.get_audios(post)
    assert len(res) == 1
    assert res[0].get('audio') == audio1.audio


@pytest.mark.django_db
def test_post_serializers_get_pics():
    post = mixer.blend(Post)
    pic2 = mixer.blend(PostPicture)
    pic1 = mixer.blend(PostPicture, post=post)
    postSerializer = PostSerializer()
    res = postSerializer.get_pics(post)
    assert len(res) == 1
    assert res[0].get('image') == pic1.image


@pytest.mark.django_db
def test_post_serializers_get_comments():
    post = mixer.blend(Post)
    comm1 = mixer.blend(Comment, post=post)
    comm2 = mixer.blend(Comment)
    postSerializer = PostSerializer()
    res = postSerializer.get_comments(post)
    assert len(res) == 1
    assert res[0].get('content') == comm1.content
