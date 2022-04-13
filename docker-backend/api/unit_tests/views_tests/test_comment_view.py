import pytest
from api.views import CommentViewSet
from mixer.backend.django import mixer
from api.models import Comment, Post
from api.unit_tests.views_tests.dump_request import Dump_request


@pytest.mark.django_db
def test_comment_without_queryset():
    comment1 = mixer.blend(Comment)
    comment2 = mixer.blend(Comment)
    comment3 = mixer.blend(Comment)
    commentView = CommentViewSet(request=Dump_request({}, ''))
    res = commentView.get_queryset()
    assert len(res) == 3
    assert res.first() == comment3
    assert res.last() == comment1


@pytest.mark.django_db
def test_comment_for_post():
    post1 = mixer.blend(Post)
    comment1 = mixer.blend(Comment, post=post1)
    comment3 = mixer.blend(Comment)
    comment2 = mixer.blend(Comment, post=post1)
    commentView = CommentViewSet(
        request=Dump_request({'post_id': post1.id}, '')
    )
    res = commentView.get_queryset()
    assert len(res) == 2
    assert res.first() == comment2
    assert res.last() == comment1


@pytest.mark.django_db
def test_comment_for_datetime():
    comment1 = mixer.blend(Comment)
    comment2 = mixer.blend(Comment)
    comment3 = mixer.blend(Comment)
    comment4 = mixer.blend(Comment)
    commentView = CommentViewSet(
        request=Dump_request({'datetime': comment3.date_posted}, '')
    )
    res = commentView.get_queryset()
    assert len(res) == 2
    assert res.first() == comment4
    assert res.last() == comment3
