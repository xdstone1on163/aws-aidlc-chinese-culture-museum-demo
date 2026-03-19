"""Account serializers."""
import re
from rest_framework import serializers
from .models import User, UserProfile


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=50)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已注册')
        return value

    def validate_nickname(self, value):
        if UserProfile.objects.filter(nickname=value).exists():
            raise serializers.ValidationError('该昵称已被使用')
        return value

    def validate_password(self, value):
        if not re.search(r'[a-zA-Z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError('密码必须包含字母和数字')
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次密码不一致'})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False, required=False)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if not re.search(r'[a-zA-Z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError('密码必须包含字母和数字')
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次密码不一致'})
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='profile.nickname', read_only=True)
    avatar = serializers.CharField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_verified', 'nickname', 'avatar', 'date_joined']
        read_only_fields = fields


class UserAdminSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='profile.nickname', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active', 'is_verified', 'nickname', 'date_joined', 'last_login']
        read_only_fields = fields


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar', 'bio', 'language']

    def validate_nickname(self, value):
        user = self.context['request'].user
        if UserProfile.objects.filter(nickname=value).exclude(user=user).exists():
            raise serializers.ValidationError('该昵称已被使用')
        return value


class RoleChangeSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['user', 'content_manager', 'admin'])
