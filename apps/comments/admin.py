from django.contrib import admin

from apps.comments.models import Comment


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'content_object',)
admin.site.register(Comment, CommentsAdmin)
