from django.db import models
from django.urls.conf import path
from djoser.views import UserViewSet
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Follow, User
from .serializers import UserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer

    @action(["get"], detail=False)
    def subscriptions(self, request):
        follower = User.objects.filter(follow__user=request.user)
        serializer = self.get_serializer(follower, many=True)
        return Response(serializer.data)


class ListOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


