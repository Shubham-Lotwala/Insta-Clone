from django.forms import ModelForm
from django import forms
from .models import Post,Comment,Reply

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','url', 'body']  
        labels = {
            'body': 'Caption',
            
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption', 'class': 'font1 text-4xl'}),
            'url': forms.URLInput(attrs={'placeholder': 'Add a url', 'class': 'font1 text-2xl'}),
            'title': forms.TextInput(attrs={'placeholder': 'Add a title', 'class': 'font1 text-2xl'}),
        
        }

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body',]  
        labels = {
            'body': '',

        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'class': 'font1 text-4xl'}),
            
        }



class CommentCreteForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]  
        labels = {
            'body': '',

        }
        widgets = {
            'body': forms.TextInput(attrs={'class': 'font1 text-2xl','placeholder': 'add a comment'}),
            
        }




class ReplyCreteForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body',]  
        labels = {
            'body': '',

        }
        widgets = {
            'body': forms.TextInput(attrs={'class': 'font1 text-2xl','placeholder': 'add a reply'}),
            
        }




