# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from stdimage.models import StdImageField


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True, default='')
    content = models.TextField(max_length=1000, blank=True, null=True)
    main_photo = StdImageField()

    def get_absolute_url(self):
        return reverse('album:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo = StdImageField()
    upload_date = models.DateField()

    def __str__(self):
        return self.photo

    def get_absolute_url(self):
        return reverse('album:detail', kwargs={'pk': self.album})


class FilteredPhoto(models.Model):
    primary_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    filtered_photo_url = StdImageField()

    def __str__(self):
        return self.filtered_photo_url

    def get_absolute_url(self):
        return reverse('album:photo-detail', kwargs={'pk': self.primary_photo})
