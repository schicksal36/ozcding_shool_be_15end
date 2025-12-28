from cProfile import label
from django import forms
from .models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = "__all__"
        fields = ("title", "content")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets =  {
            'content' :forms.TextInput(attrs = 
            {
                "class" : "form-control",
                "rows" : 3,
                "placeholder" : "댓글을 입력하세요"
            
            })}
        
        labels = {
            'content' : '댓글'
        }
 