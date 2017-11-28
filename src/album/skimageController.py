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


class FileCommand(object):
    @classmethod
    def getTempPath(cls, filename):
        return os.path.join(settings.MEDIA_ROOT, filename)

    @classmethod
    def imageToNumArray(cls, filepath):
        return io.imread(filepath)


class SkimageRgb2GrayCommands(FileCommand):
    @classmethod
    def execute(cls, **kwargs):

        file = kwargs.get('filename')
        tmp_file = cls.getTempPath(file.name)

        img = cls.imageToNumArray(tmp_file)

        img_gray = rgb2gray(img)

        img_gray_path = 'rgb2gray_' + file.name

        return img_gray_path, img_gray


FILTERS = {
        'RGB2GRAY': SkimageRgb2GrayCommands,
    }

class SkimageController(object):
    @classmethod
    def uploadImage(cls, **kwargs):

        params = {
            'filename': kwargs.get('filename'),
        }

        filter = kwargs.get('filterFn')
        image_path, image = FILTERS[filter].execute(**params)
        try:
            scipy.misc.imsave(settings.MEDIA_ROOT + '/' + image_path, image)
            return image_path

        except:
            return 0