from rest_framework import serializers
from django.contrib.auth.models import User
from article.models import Article
from user.models import Profile


class UserSerializer(serializers.ModelSerializer):
    # profile = serializers.PrimaryKeyRelatedField(read_only=True)
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())
    type = serializers.CharField(source='profile.type')
    biography = serializers.CharField(source='profile.biography')
    avatar = serializers.CharField(source='profile.avatar')
    name = serializers.CharField(source='profile.name')
    sid = serializers.CharField(source='profile.sid')

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'articles', 'type', 'biography', 'avatar', 'name', 'sid')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = (
            'user', 'username', 'created_at', 'updated_at', 'type',
            'biography', 'avatar', 'name', 'sid'
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'type', 'biography', 'avatar', 'name', 'sid'
        )

    def validate_type(self, value):
        if value not in ['普通用户', '队员', '教练', '退役队员']:
            raise serializers.ValidationError("用户类型不正确")
        return value
