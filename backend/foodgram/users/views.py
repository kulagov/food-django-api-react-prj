from django.db import models
from django.urls.conf import path
from djoser.views import UserViewSet
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Follow, User
from .serializers import UserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    permission_classes = None

    @action(['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def subscriptions(self, request):
        follower = User.objects.filter(follow__user=request.user)
        serializer = self.get_serializer(follower, many=True)
        return Response(serializer.data)

    @action(['get'], detail=False)
    def me(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(['get', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        queryset = User.objects.all()
        follow = get_object_or_404(queryset, id=id)
        if request.method == 'GET':
            Follow.objects.get_or_create(
                user=request.user,
                following=follow,
            )
        elif request.method == 'DELETE':
            try:
                following = Follow.objects.get(
                    user=request.user,
                    following=follow
                )
                following.delete()
            except Exception:
                return Response(
                    {'errors': 'Вы не подписаны на этого пользователя', },
                    status.HTTP_400_BAD_REQUEST
                )
        serializer = self.get_serializer(follow)
        return Response(serializer.data)


class ListOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass
