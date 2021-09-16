from django.db import models
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import fields, serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User

    def get_is_subscribed(self, obj):
        # follower = get_object_or_404(obj.follow, id=self.context['request'].user.id)
        # return follower.user == self.context['request'].user
        try:
            out = self.context['request'].user.follower.all().get(following=obj)
            return True
        except:
            return False

# потом убрать в настройках djoser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


# class CustomUserSerializer(UserSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             # 'is_subscribed'
#         )
