from django.contrib import admin
from mainapp.models import VGUser, PostVGUser

@admin.register(VGUser)
class VGUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')


@admin.register(PostVGUser)
class PostVGUserAdmin(admin.ModelAdmin):
    list_display = ('description', 'author')

