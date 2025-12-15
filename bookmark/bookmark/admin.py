from django.contrib import admin
from .models import Bookmark
# Register your models here.

@admin.register(Bookmark)
#admin.site.register(Bookmark,BookmarkAdmin)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ['name','url']
    list_filter = ['name']

