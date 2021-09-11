from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet

router_v1 = DefaultRouter()
router_v1.register('users/subscriptions/', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    # path('users/subscriptions/', FollowViewSet.as_view()),
]
