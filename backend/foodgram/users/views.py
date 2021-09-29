from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import UserFollowSerializer

from .models import Follow, User
from .serializers import UserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = LimitOffsetPagination

    @action(['get'], detail=False)
    def subscriptions(self, request):
        follower = User.objects.filter(follow__user=request.user)
        page = self.paginate_queryset(follower)
        serializer = UserFollowSerializer(
            page,
            many=True,
            context={'user': request.user})
        return self.get_paginated_response(serializer.data)

    @action(['get'], detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user)
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
            except ValueError:
                return Response(
                    {'errors': 'Вы не подписаны на этого пользователя', },
                    status.HTTP_400_BAD_REQUEST
                )
        serializer = self.get_serializer(follow)
        return Response(serializer.data)
