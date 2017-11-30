# -*- coding: utf-8 -*-

from django.views.generic import View
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from Album_na_Zdjecia.authController import SecuredUser
from django.core.urlresolvers import reverse_lazy
from .models import Album, Photo, FilteredPhoto
from .forms import PhotoForm, AlbumForm
from .skimageCommands import SkimageController, FILTERS


class IndexView(SecuredUser, generic.ListView):
    form_class = AlbumForm
    template_name = 'album/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.filter(user_id=self.request.user.id)


class DetailView(SecuredUser, generic.DetailView):
    model = Album
    template_name = 'album/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id == self.request.user.id:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return redirect('album:index')


class AlbumCreate(SecuredUser, CreateView):
    form_class = AlbumForm
    template_name = 'album/album_form.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = User.objects.get(id=request.user.id)

        if form.is_valid():
            form.save()

        return redirect('album:index')


class AlbumDelete(SecuredUser, DeleteView):
    model = Album
    success_url = reverse_lazy('album:index')

    def post(self, request, *args, **kwargs):
        params = {
            'albumTitle': request.POST['album_title'],
            'main_photo': request.POST['main_photo'],
        }

class PhotoView(SecuredUser, generic.DetailView):
    model = Photo
    template_name = 'album/photo_detail.html'

    def get(self, request, *args, **kwargs):
        super(PhotoView, self).checkSession(self, request, *args, **kwargs)
        if Album.objects.filter(pk=self.object.album_id, user_id=self.request.user.id):
            return self.render_to_response(self.get_context_data(object=self.object))
        else:
            return redirect('album:index')


class PhotoDelete(SecuredUser, View):
    model = Photo
    success_url = reverse_lazy('album:index')

    def post(self, request, *args, **kwargs):

        res = Photo.objects.filter(id=kwargs.get('photo_id')).delete()

        return redirect('album:detail', pk=kwargs.get('pk'))


class PhotoFormView(SecuredUser, CreateView):
    form_class = PhotoForm
    template_name = 'album/photo_form.html'

    def post(self, request, *args, **kwargs):
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














