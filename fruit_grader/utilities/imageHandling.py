import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from segritech import settings


def getPathAbsolute(pathRelative):
    return os.path.join(settings.MEDIA_ROOT, pathRelative)


def storeImageToLocal(img):
    imgName = img.name
    imgPathRelative = default_storage.save(imgName, ContentFile(img.read()))
    return imgPathRelative


def deleteFileFromLocal(absolutePath):
    os.remove(absolutePath)


def addGradesToImageName(imagePathAbsolute, score, label):

    imagePath = imagePathAbsolute.split('.')
    imagePathAndName = imagePath[0]
    imageExtension = imagePath[1]

    gradedImagePathAbsolute = imagePathAndName + '_' + 'score=' + str(score) + '_' + 'grade=' + label + '.' + imageExtension
    return gradedImagePathAbsolute
