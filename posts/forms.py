from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': "What's on your mind?", 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm', 'style': 'max-width:220px;'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Write a comment...'}),
        }
