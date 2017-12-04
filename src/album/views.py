# -*- coding: utf-8 -*-

from django.views.generic import View
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView
from requests import request as req

from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from .models import Album, Photo, FilteredPhoto
from .forms import PhotoForm, AlbumForm
from .skimageCommands import SkimageController, FILTERS, FileController
from allauth.socialaccount.models import SocialAccount, SocialToken


class IndexView(generic.ListView):
    form_class = AlbumForm
    template_name = 'album/index.html'
    context_object_name = 'album_list'

    def get(self, request, *args, **kwargs):
        res = SocialAccount.objects.filter(provider='facebook', user_id=request.user.id)
        if res:
            user = ""
            token = SocialToken.objects.get(account_id=SocialAccount.objects.get(user_id=request.user.id))

            res = req('get', 'https://graph.facebook.com/v2.11/me?fields=id,name&access_token='+token.token)
        return super(IndexView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        return Album.objects.filter(user_id=self.request.user.id)


class DetailView(generic.DetailView):
    model = Album
    template_name = 'album/detail.html'

    def get(self, request, *args, **kwargs):
        super(DetailView, self).get(self, request, *args, **kwargs)
        if self.object.user_id == self.request.user.id:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return redirect('album:index')


class AlbumCreate(CreateView):
    form_class = AlbumForm
    template_name = 'album/album_form.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = User.objects.get(id=request.user.id)

        if form.is_valid():
            form.save()

        return redirect('album:index')


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('album:index')

    def post(self, request, *args, **kwargs):
        try:
            FileController.deleteAlbum(Album.objects.get(id=kwargs.get('pk')))
            return redirect('album:index')
        except:
            return redirect('album:index')


class PhotoView(generic.DetailView):
    model = Photo
    template_name = 'album/photo_detail.html'

    def get(self, request, *args, **kwargs):
        super(PhotoView, self).get(self, request, *args, **kwargs)
        if Album.objects.filter(pk=self.object.album_id, user_id=self.request.user.id):
            res = self.get_context_data(object=self.object)
            return self.render_to_response(res)
        else:
            return redirect('album:index')


class PhotoDelete(View):
    model = Photo
    success_url = reverse_lazy('album:index')

    def post(self, request, *args, **kwargs):
        try:
            res = Photo.objects.filter(id=kwargs.get('photo_id'))
            FileController.deletePhoto(res)
            res.delete()
            return redirect('album:detail', pk=kwargs.get('pk'))
        except:
            return redirect('album:detail', pk=kwargs.get('pk'))


class PhotoCreate(CreateView):
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
                photo_form.filter_photo = filter_image
                filt_form = FilteredPhoto(primary_photo=form.instance, filtered_photo_url=filter_image)
                filt_form.save()

        return redirect('album:detail', pk=request.GET['album_id'])














