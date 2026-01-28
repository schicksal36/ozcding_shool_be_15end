from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = "__all__"
        fields = ("title", "content", "category", "image")  
        widgets = {
            # ✅ Summernote 적용
            "content": SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            # ❌ TextInput + rows → 오류
            # ✅ Textarea 사용
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "댓글을 입력하세요",
                }
            )
        }
        labels = {
            "content": "댓글",
        }
