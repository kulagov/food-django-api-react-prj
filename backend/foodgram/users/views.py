from django.db import models
from django.urls.conf import path
from djoser.views import UserViewSet
from rest_framework import generics, mixins, viewsets
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Follow, User
from .serializers import UserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer


class ListOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


