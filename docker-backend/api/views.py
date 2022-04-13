from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions

from api.serializers import (
    UserSerializer,
    GroupSerializer,
    PostSerializer,
    ProfileSerializer,
    PostPictureCRUDSerializer,
    PostAudioCRUDSerializer,
    CommentSerializer,
)
from api.permissions import (
    AuthorAndStaffEdit,
    NoDeletePermission,
    DenyAccesToOtherUsersProfiles,
    AllowCreateProfileWithoutAuthentication,
    UpdateOrDeleteOnly,
    CreateAndGetOnlyStaffFullAccess,
)

from api.models import PostAudio, Profile, Post, PostPicture, Comment

import boto3
from botocore.client import Config
from DjangoBlogTutorial import settings


def get_search_result(request):
    search_request = request.GET['request']

    search_users = Profile.objects.filter(
        user__username__icontains=search_request
    )
    profile_serializer = ProfileSerializer(search_users, many=True)

    search_posts = Post.objects.filter(
        Q(title__icontains=search_request)
        | Q(content__icontains=search_request)
    )
    post_serializer = PostSerializer(search_posts, many=True)

    search_comments = Comment.objects.filter(content__icontains=search_request)
    comment_serializer = CommentSerializer(search_comments, many=True)

    return JsonResponse(
        {
            'search users': profile_serializer.data,
            'search post': post_serializer.data,
            'search comments': comment_serializer.data,
        }
    )


def get_upload_url(filename):
    s3_signature = {'v4': 's3v4', 'v2': 's3'}
    client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version=s3_signature['v4']),
        region_name='us-east-1',
    )
    url = client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': filename,
            'ACL': 'public-read',
        },
        ExpiresIn=100000,
    )
    return url


def createUploadLink(request):
    filename = request.GET['filename']
    return JsonResponse({'url': get_upload_url(filename)})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        NoDeletePermission,
        DenyAccesToOtherUsersProfiles
        | AllowCreateProfileWithoutAuthentication,
    ]

    def get_queryset(self):
        get_self = self.request.query_params.get('self')
        if get_self:
            return self.queryset.filter(user_id=self.request.user.id)
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user_id=self.request.user.id)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    permission_classes = [
        AuthorAndStaffEdit,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        res = self.request.query_params.get('author')
        if res:
            return self.queryset.filter(author__username=res)
        return self.queryset


class PostPicViewSet(viewsets.ModelViewSet):
    queryset = PostPicture.objects.all()
    serializer_class = PostPictureCRUDSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        UpdateOrDeleteOnly,
    ]


class PostAudioViewSet(viewsets.ModelViewSet):
    queryset = PostAudio.objects.all()
    serializer_class = PostAudioCRUDSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        UpdateOrDeleteOnly,
    ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-date_posted')
    serializer_class = CommentSerializer
    permission_classes = [
        CreateAndGetOnlyStaffFullAccess,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        datetime = self.request.query_params.get('datetime')
        post_id = self.request.query_params.get('post_id')
        res = self.queryset
        if post_id:
            res = res.filter(post_id=post_id)
        if datetime:
            res = res.filter(date_posted__gte=datetime)
        return res
