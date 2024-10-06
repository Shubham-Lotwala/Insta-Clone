from django.forms import ModelForm
from django import forms
from users.models import Profile

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude=['user']
        labels={
            'name': 'Name'
        }
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image':forms.FileInput()
        }