from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = __all__ 전체 적용시
        fields = ("title", "content")
