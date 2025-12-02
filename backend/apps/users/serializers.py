"""User serializers."""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'show_thinking', 'theme', 'preferences']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UpdateProfileSerializer(serializers.Serializer):
    display_name = serializers.CharField(required=False, allow_blank=True)
    show_thinking = serializers.BooleanField(required=False)
    theme = serializers.CharField(required=False)
    preferences = serializers.JSONField(required=False)

    def update(self, instance, validated_data):
        profile = instance.profile
        for key, value in validated_data.items():
            setattr(profile, key, value)
        profile.save()
        return instance
