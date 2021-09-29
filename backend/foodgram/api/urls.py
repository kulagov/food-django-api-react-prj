from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import (
    ComponentViewSet, IngredientViewSet, RecipeViewSet, TagViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeViewSet)
router_v1.register('components', ComponentViewSet)


urlpatterns = [
    path('', include('users.urls')),
    path('', include(router_v1.urls)),
]
