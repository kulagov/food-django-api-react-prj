from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username', 'first_name', 'last_name')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
