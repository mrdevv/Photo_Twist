
from django.conf.urls import url
from . import views

app_name = 'album'

urlpatterns = [
    # /album/
    url(r'^$', views.IndexView.as_view(), name='index'),

    #/album/<album_id>
    url(r'^(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='detail'),

    # /album/<album_id>/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),

    #/album/add
    url(r'^add/$', views.AlbumCreate.as_view(), name='album-add'),

    # /album/<album_id>/add
    url(r'^add-photo/$', views.PhotoFormView.as_view(), name='photo-add'),

    # /album/<album_id>/delete/<photo_id>
    url(r'^(?P<pk>[0-9]+)/(?P<photo_id>[0-9]+)/delete/$', views.PhotoDelete.as_view(), name='photo-delete'),

    # /album/<album_id>/photo/<photo_id>
    url(r'^photo/(?P<pk>[0-9]+)/$', views.PhotoView.as_view(), name='photo-detail'),

]