from django.contrib import admin

from .models import Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('measurement_unit', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
