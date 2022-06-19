from django.contrib import admin

from .models import BlogPost, Profile


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'author']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Profile, ProfileAdmin)

