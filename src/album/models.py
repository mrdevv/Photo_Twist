# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse


class Album(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    content = models.TextField(max_length=1000, blank=True, null=True)
    main_photo = models.FileField()

    def get_absolute_url(self):
        return reverse('album:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo = models.FileField()
    filter_photo = models.CharField(max_length=100, null=True, blank=True)
    upload_date = models.DateField()

    def __str__(self):
        return self.photo

    def get_absolute_url(self):
        return reverse('album:detail', kwargs={'pk': self.album})
