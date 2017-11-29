# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings

from django.core.urlresolvers import reverse_lazy
from .models import Album, Photo, FilteredPhoto
from .forms import PhotoForm
from .skimageController import SkimageController, FILTERS, FileController



class IndexView(generic.ListView):
    template_name = 'album/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'album/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['title', 'date', 'content', 'main_photo']

    def post(self, *args, **kwargs):
        try:
            FileController.createAlbum(**{'albumTitle': self.request.POST['title']})
            return super(AlbumCreate, self).post(self, *args, **kwargs)
        except:
            pass


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('album:index')

    def post(self, request, *args, **kwargs):
        params = {
            'albumTitle': request.POST['album_title'],
            'main_photo': request.POST['main_photo'],
        }

        try:
            FileController.deleteAlbum(**params)
            return self.delete(request, *args, **kwargs)

        except:
            return self.delete(request, *args, **kwargs)


class PhotoView(generic.DetailView):
    model = Photo
    template_name = 'album/photo_detail.html'


class PhotoDelete(View):
    model = Photo
    success_url = reverse_lazy('album:index')

    def post(self, request, *args, **kwargs):

        res = Photo.objects.filter(id=kwargs.get('photo_id')).delete()

        return redirect('album:detail', pk=kwargs.get('pk'))


class PhotoCreate(View):
    form_class = PhotoForm
    template_name = 'album/photo_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            photo_form = form.save()

            for key, value in FILTERS.items():
                filter_image = SkimageController.uploadImage(filename=photo_form.photo,
                                                             albumpath=photo_form.album.title,
                                                             filterFn=key)
                photo_form.filter_photo = settings.MEDIA_URL + filter_image
                filt_form = FilteredPhoto(primary_photo=form.instance, filtered_photo_url=settings.MEDIA_URL + filter_image)
                filt_form.save()


        return redirect('album:detail', pk=request.GET['album_id'])
