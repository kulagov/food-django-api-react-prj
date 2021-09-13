from django.db import models
from django.urls.conf import path
from djoser.views import UserViewSet
from rest_framework import generics, mixins, viewsets
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Follow, User
from .serializers import CustomUserSerializer, FollowSerializer, UserSerialiser

# class CustomUserViewSet(UserViewSet):  # удалить
#     serializer_class = CustomUserSerializer  # удалить


class ListOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


class UserViewSet(ListOrCreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiser


class FollowViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    # model = Follow


class F1ollowViewSet(ListOrCreateViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    # permission_classes = [IsAuthenticated, UserIsAuthor]
    # filter_backends = [SearchFilter]
    # search_fields = ['=user__username', ]

    # def get_queryset(self):
    #     queryset = self.request.user
    #     return queryset

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
