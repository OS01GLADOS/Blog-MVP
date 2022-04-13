import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from api.serializers import CommentSerializer
from api.models import Post, Comment
from api.unit_tests.views_tests.dump_request import Dump_request


@pytest.mark.django_db
def test_comments_serializer():
    user = mixer.blend(User)
    post = mixer.blend(Post)
    comment = CommentSerializer(context={'request': Dump_request({}, user)})
    validated_data = {'content': 'dfglkdujfhhltr4ydfgb', 'post': post}
    res = comment.create(validated_data=validated_data)
    assert res == Comment.objects.all().first()
