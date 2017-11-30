import skimage
import shutil
import numpy
import scipy.misc
import os

from skimage import io, data, img_as_float, color
from skimage.color import rgb2gray
from skimage.filters import roberts, sobel, scharr, prewitt
from skimage.morphology import watershed
from skimage.measure import label
from skimage.segmentation import slic, join_segmentations
from numpy import transpose

from django.conf import settings


class FileCommand(object):
    @classmethod
    def getTempPath(cls, filename):
        return os.path.join(settings.MEDIA_ROOT, filename)

    @classmethod
    def imageToNumArray(cls, filepath):
        return io.imread(filepath)

    @classmethod
    def deleteFullAlbum(cls, albumpath, filepath):
        os.remove(filepath)
        shutil.rmtree(albumpath)
        return


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

        img_gray = roberts(img)

        img_gray_path = 'edge_' + file.name

        return img_gray_path, img_gray


class SkimageColorCommand(FileCommand):
    @classmethod
    def execute(cls, **kwargs):

        file = kwargs.get('filename')
        tmp_file = cls.getTempPath(file.name)
        img = cls.imageToNumArray(tmp_file)

        img_grey = rgb2gray(img)


        img_edge = roberts(img_grey)
        imgFloat = img_as_float(img_edge[::2, ::2])
        img_color = color.gray2rgb(imgFloat)
        red_color = [1, 0, 0]
        edge_res = img_color * red_color

        img_path = 'color_' + file.name

        return img_path, edge_res


FILTERS = {
        'RGB2GRAY': SkimageRgb2GrayCommands,
        'EDGE': SkimageEdgeCommand,
        'COLOR': SkimageColorCommand,
    }


class SkimageController(object):
    @classmethod
    def uploadImage(cls, **kwargs):

        params = {
            'filename': kwargs.get('filename'),
        }

        filter = kwargs.get('filterFn')
        album_path = kwargs.get('albumpath')
        image_path, image = FILTERS[filter].execute(**params)
        dir = os.path.join(settings.MEDIA_ROOT, album_path)

        path = os.path.join(dir, image_path)

        try:
            scipy.misc.imsave(path, image)
            return image_path

        except:
            return 0


class FileController(FileCommand):
    @classmethod
    def deleteAlbum(cls, **kwargs):

        try:
            albumpath = os.path.join(settings.MEDIA_ROOT, kwargs.get('albumTitle'))
            filepath = os.path.join(settings.MEDIA_ROOT, kwargs.get('main_photo'))
            FileCommand.deleteFullAlbum(albumpath, filepath)
        except:
            return 1

    @classmethod
    def createAlbum(cls, **kwargs):
        albumpath = kwargs.get('albumTitle')
        dir = os.path.join(settings.MEDIA_ROOT, albumpath)
        try:
            os.stat(dir)
        except:
            os.makedirs(dir)

        return 1
