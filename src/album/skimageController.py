import skimage
from skimage import io, data
from skimage.color import rgb2gray
import numpy
import PIL
from PIL import Image
import shutil
import scipy.misc
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class SkimageCommand(object):
    @staticmethod
    def uploadImage(filename=None, *args, **kwargs):

        #przygotowanie oryginalnego pliku w katalogu tmp
        tmp_file = os.path.join(settings.MEDIA_ROOT, filename.name)

        moon = io.imread(tmp_file)
        img_rgb = rgb2gray(moon)

        #zapis obrazu jako tablica, numpy
        scipy.misc.imsave(settings.MEDIA_ROOT + '/' + filename.name, img_rgb)


        return 0