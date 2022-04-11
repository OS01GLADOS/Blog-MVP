from django.test import TestCase
from api.models import Post, Comment
from django.contrib.auth.models import User
from mixer.backend.django import mixer


class TestProfileModel(TestCase):
    def setUp(self):
        self.new_user = mixer.blend(User)

    def test_add_a_plus_b(self):
        a = 1
        b = 2
        c = a + b
        assert c == 3

    def test_profile_create(self):
        new_user_profile = self.new_user.profile
        self.assertEqual(
            new_user_profile.user.username, self.new_user.username
        )

    def test_string_return(self):
        profile = self.new_user.profile
        assert str(profile) == self.new_user.username + ' Profile'


class TestPostModels(TestCase):
    def setUp(self):
        self.new_user = mixer.blend(User)
        self.new_post = mixer.blend(Post)

    def test_get_absolute_url(self):
        assert (
            self.new_post.get_absolute_url()
            == f'/api/posts/{self.new_post.id}/'
        )

    def test_post_str_method(self):
        assert self.new_post.title == str(self.new_post)


class TestCommentModel(TestCase):
    def setUp(self):
        self.new_comment = mixer.blend(Comment)

    def test_comment_str_method(self):
        assert (
            str(self.new_comment)
            == f'Comment {self.new_comment.id} on post {self.new_comment.post.title}'
        )
