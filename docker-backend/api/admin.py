from django.contrib import admin

# Register your models here.
from api.models import Comment, Post, PostPicture, Profile, PostAudio

admin.site.register(Post)
admin.site.register(PostPicture)
admin.site.register(PostAudio)
admin.site.register(Profile)
admin.site.register(Comment)
