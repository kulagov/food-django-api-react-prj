from django.db import router
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, loaddata

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router_v1.urls)),
    # path('loaddata/', loaddata),
]
