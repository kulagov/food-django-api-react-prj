from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'id': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'is_subscribed': {'required': True}
        }

    def get_is_subscribed(self, obj):
        if obj.is_anonymous:
            return False
        try:
            user = self.context['request'].user
        except KeyError:
            user = self.instance
        return Follow.objects.filter(user=user, following=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
