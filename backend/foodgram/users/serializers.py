from django.db import models
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import fields, serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = 'username', 'id', 'email'
        fields = '__all__'
        model = User


class UserSerialiser(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class F_ollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    # def validate(self, attrs):
    #     if (
    #         attrs['user'] == attrs['following']
    #         and self.context['request'].method == 'GET'
    #     ):
    #         raise serializers.ValidationError(
    #             'Вы не можете подписаться сами на себя.'
    #         )
    #     return attrs

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Уже подписаны.'
            )
        ]


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed'
        )
