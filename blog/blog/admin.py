from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Blog, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ("author", "content")
    extra = 1


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields  = ['content',]
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "blog", "author", "created_at")
    list_filter = ("blog", "author")
    search_fields = ("content",)
