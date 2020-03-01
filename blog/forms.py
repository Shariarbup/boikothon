from django import forms
from .models import Article, Author , Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]

class userRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
class createAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'details',
            'profile_picture',
            
        ]

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'post_comment',    
        ]