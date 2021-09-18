from django.contrib import admin
from django.db import models

from .models import Ingredient, Recipe, Tag, Component


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('measurement_unit', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')


class ComponentInline(admin.TabularInline):
    model = Component


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tag')
    inlines = [ComponentInline, ]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
