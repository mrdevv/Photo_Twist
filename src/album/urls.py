
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'album'

urlpatterns = [

    # /album/
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),

    #/album/<album_id>
    url(r'^(?P<pk>[0-9]+)$', login_required(views.DetailView.as_view()), name='detail'),

    # /album/<album_id>/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.AlbumDelete.as_view()), name='album-delete'),

    #/album/add
    url(r'^add/$', login_required(views.AlbumCreate.as_view()), name='album-add'),

    # /album/<album_id>/add
    url(r'^add-photo/$', login_required(views.PhotoCreate.as_view()), name='photo-add'),

    # /album/<album_id>/delete/<photo_id>
    url(r'^(?P<pk>[0-9]+)/(?P<photo_id>[0-9]+)/delete/$', login_required(views.PhotoDelete.as_view()), name='photo-delete'),

    # /album/<album_id>/photo/<photo_id>
    url(r'^photo/(?P<pk>[0-9]+)/$', login_required(views.PhotoView.as_view()), name='photo-detail'),

]