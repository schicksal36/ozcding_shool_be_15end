from django.contrib import admin
from .models import Blog, Comment


class CommentInline(admin.TabularInline):
    model = Comment            # 기본 표시 개수
    fields = ("author", "content")
    extra = 1



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]
