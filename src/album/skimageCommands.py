import shutil
import numpy
import scipy.misc
import os

from skimage import io, data, img_as_float, color, transform
from skimage.color import rgb2gray, gray2rgb
from skimage.filters import roberts, sobel, scharr, prewitt, rank
from skimage.morphology import watershed, erosion, dilation
from skimage.measure import label
from skimage.segmentation import slic, join_segmentations
from numpy import transpose
from .models import FilteredPhoto, Photo, Album
from stdimage.utils import pre_delete_delete_callback

from django.conf import settings


class FileCommand(object):
    @classmethod
    def getTempPath(cls, filename):
        return os.path.join(settings.MEDIA_ROOT, filename)

    @classmethod
    def imageToNumArray(cls, filepath):
        # change image to 3-d array
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


class SkimageEdgeCommand(FileCommand):
    @classmethod
    def execute(cls, **kwargs):

        file = kwargs.get('filename')
        tmp_file = cls.getTempPath(file.name)

        img = cls.imageToNumArray(tmp_file)
        img = rgb2gray(img)

        img_gray = sobel(img)

        img_gray = dilation(img_gray, numpy.ones([3,3]))

        img_gray_path = 'edge_' + file.name

        return img_gray_path, img_gray


class SkimageColorCommand(FileCommand):
    @classmethod
    def execute(cls, **kwargs):

        file = kwargs.get('filename')
        tmp_file = cls.getTempPath(file.name)
        img = cls.imageToNumArray(tmp_file)

        img_grey = rgb2gray(img)

        img_edge = sobel(img_grey)
        imgFloat = img_as_float(img_edge[::2, ::2])
        img_color = color.gray2rgb(imgFloat)
        red_color = [1, 0, 0]
        edge_res = img_color * red_color

        img_path = 'color_' + file.name

        return img_path, edge_res


class SkimageColorMedianCommands(FileCommand):
    @classmethod
    def execute(cls, **kwargs):

        file = kwargs.get('filename')
        tmp_file = cls.getTempPath(file.name)

        img = cls.imageToNumArray(tmp_file)
        img_gray = rgb2gray(img)

        img_median = rank.median(img_gray, numpy.ones([8,8], dtype=numpy.uint8))

        img_gray_path = 'median_' + file.name

        return img_gray_path, img_median



FILTERS = {
        'RGB2GRAY': SkimageRgb2GrayCommands,
        'EDGE': SkimageEdgeCommand,
        'COLOR': SkimageColorCommand,
        'MEDIAN': SkimageColorMedianCommands,
    }


class SkimageController(object):
    @classmethod
    def uploadImage(cls, **kwargs):

        params = {
            'filename': kwargs.get('filename'),
        }

        filter = kwargs.get('filterFn')
        image_path, image = FILTERS[filter].execute(**params)
        dir = os.path.join(settings.MEDIA_ROOT, image_path)

        try:
            scipy.misc.imsave(dir, image)
            return image_path
        except:
            return 0


class FileController(FileCommand):
    @classmethod
    def deleteAlbum(cls, album):
        photos = Photo.objects.filter(album_id=album.id)
        if photos:
            cls.deletePhoto(photos)
        pre_delete_delete_callback(sender=Album, instance=album)
        album.delete()
        return True

    @classmethod
    def deletePhoto(cls, photos):
        for foto in photos:
            filt = FilteredPhoto.objects.filter(primary_photo_id=foto.id)
            pre_delete_delete_callback(sender=Photo, instance=foto)
            for i in filt:
                pre_delete_delete_callback(sender=FilteredPhoto, instance=i)
        return True

    @classmethod
    def deleteFilteredPhotos(cls, **kwargs):
        pass