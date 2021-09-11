from django.urls.conf import path
from djoser.views import UserViewSet
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .serializers import CustomUserSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):  # удалить
    serializer_class = CustomUserSerializer  # удалить


class ListOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


class FollowViewSet(ListOrCreateViewSet):
    serializer_class = FollowSerializer
    # permission_classes = [IsAuthenticated, UserIsAuthor]
    # filter_backends = [SearchFilter]
    search_fields = ['=user__username', ]

    def get_queryset(self):
        queryset = self.request.user.follow
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
