from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Profile, Post, PostPicture, PostAudio, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(
        required=False, source="user.username", read_only=False
    )
    email = serializers.EmailField(
        required=False, source="user.email", read_only=False
    )
    password = serializers.CharField(required=False)
    profile_id = serializers.IntegerField(source="id", read_only=True)
    id = serializers.IntegerField(source="user.id", read_only=True)
    registration_date = serializers.DateTimeField(
        source="user.date_joined", read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            'id',
            'profile_id',
            'username',
            'email',
            'password',
            'image',
            'registration_date',
        ]

    def get_validation_exclusions(self):
        exclusions = super(ProfileSerializer, self).get_validation_exclusions()
        return exclusions + ['password']

    def update(self, instance, validated_data):
        if validated_data.get('user'):
            updated_user = validated_data.get('user')

            instance.user.username = updated_user.get(
                'username', instance.user.username
            )
            instance.user.email = updated_user.get(
                'email', instance.user.email
            )

        if validated_data.get('image'):
            instance.image = validated_data.get('image')
        new_password = validated_data.get('password')
        if new_password:
            instance.user.set_password(new_password)
        instance.user.save()
        instance.save()
        return instance

    def create(self, validated_data):
        new_user = validated_data.get('user')
        password = validated_data.get('password')
        user = User(
            username=new_user.get('username'), email=new_user.get('email')
        )
        user.set_password(password)
        user.save()

        return user.profile


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostAudioCRUDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostAudio
        fields = '__all__'


class PostAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAudio
        fields = ['audio', 'audio_number', 'audio_name']


class PostPictureCRUDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostPicture
        fields = '__all__'


class PostPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPicture
        fields = ['image', 'image_number']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author_username = serializers.CharField(
        source="author.username", read_only=True
    )
    author_id = serializers.IntegerField(source="author.id", read_only=True)
    date_posted = serializers.DateTimeField(read_only=True)
    pics = serializers.SerializerMethodField()
    audios = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_audios(self, obj):
        results = PostAudio.objects.filter(post__id=obj.id)
        return PostAudioSerializer(results, many=True).data

    def get_pics(self, obj):
        results = PostPicture.objects.filter(post__id=obj.id)
        return PostPictureSerializer(results, many=True).data

    def get_comments(self, obj):
        results = Comment.objects.filter(post__id=obj.id).order_by(
            '-date_posted'
        )
        return CommentSerializer(results, many=True).data

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'date_posted',
            'author_id',
            'author_username',
            'comments',
            'pics',
            'audios',
        ]

    def create(self, validated_data):
        new_post = Post()
        new_post.author = self.context['request'].user
        new_post.title = validated_data.get('title')
        new_post.content = validated_data.get('content')
        new_post.save()
        return new_post

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source="sender.username", read_only=True
    )
    sender_id = serializers.IntegerField(source="sender.id", read_only=True)
    sender_image = serializers.CharField(
        source='sender.profile.image', read_only=True
    )
    date_posted = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'sender_id',
            'sender_username',
            'sender_image',
            'date_posted',
            'content',
            'post',
        ]

    def create(self, validated_data):
        new_comment = Comment()
        new_comment.sender = self.context['request'].user
        new_comment.content = validated_data.get('content')
        new_comment.post = validated_data.get('post')
        new_comment.save()
        return new_comment
