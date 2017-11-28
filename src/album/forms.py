
from .models import Album, Photo
from django import forms
from django.db import models


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'date', 'content', 'main_photo']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'photo', 'upload_date']
