from cProfile import label
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm): 
    class Meta:
        model = Post
        fields = ['post_image', 'text']


class CommentForm(forms.ModelForm): 
    text = forms.CharField(label="Type your comment", widget=forms.Textarea(
        attrs={
            'placeholder':'Say somthing',
            'style':"width: 24rem; height: 6rem;"
        }
    ))
    
    class Meta:
        model = Comment
        fields = ['text']
