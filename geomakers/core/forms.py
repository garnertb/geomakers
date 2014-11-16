from .models import Image, Project, UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description', 'location', 'facebook', 'twitter', 'linkedin', 'picture')

class ContributeForm(forms.ModelForm):
    class Meta:
        model = Project
#        fields = ('typeOfProject', 'title', 'abstract', 'location', 'images', 'videos', 'links', 'related')
        fields = ('typeOfProject', 'title', 'abstract', 'location')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields =('image', 'caption')
