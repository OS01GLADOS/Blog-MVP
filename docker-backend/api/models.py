from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostPicture(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='pics'
    )
    image = models.CharField(max_length=500, null=True)
    image_number = models.IntegerField(default=1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(
        max_length=500,
        default="https://os01glados-django-blog-statics.s3.amazonaws.com/default.jpg",
    )

    def __str__(self):
        return f'{self.user.username} Profile'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return f'Comment {self.id} on post {self.post.title}'

    class Meta:
        ordering = ['date_posted']
