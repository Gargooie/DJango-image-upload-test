from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    avatar = forms.ImageField(label='Фото профиля', required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar')


class ProfilePageForm(forms.ModelForm):
    about_me = forms.CharField(max_length=500, label='Обо мне', required=False, widget=forms.Textarea)
    avatar = forms.FileField(label='Фото профиля', required=False)

    class Meta:
        model = User
        fields = ['avatar', 'about_me', 'first_name', 'last_name', 'email']


class CreatePostForm(forms.Form):
    content = forms.CharField(label='Содержание', widget=forms.Textarea)


class PhotosLoadForm(forms.Form):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class UploadPostsFile(forms.Form):
    posts = forms.FileField()
