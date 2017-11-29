
from .models import Album, Photo, FilteredPhoto
from django import forms


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'date', 'content', 'main_photo']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'photo', 'upload_date']


class FilteredPhotoForm(forms.ModelForm):
    class Meta:
        model = FilteredPhoto
        fields = '__all__'


