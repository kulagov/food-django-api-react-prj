from django.db import models
from django.urls.conf import path
from djoser.views import UserViewSet
from rest_framework import generics, mixins, viewsets, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import UserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer

    @action(["get"], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # self.request.user.set_password(serializer.data["new_password"])
        # self.request.user.save()

        # if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
        #     context = {"user": self.request.user}
        #     to = [get_user_email(self.request.user)]
        #     settings.EMAIL.password_changed_confirmation(self.request, context).send(to)

        # if settings.LOGOUT_ON_PASSWORD_CHANGE:
        #     utils.logout_user(self.request)
        # elif settings.CREATE_SESSION_ON_LOGIN:
        #     update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)




class ListOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


