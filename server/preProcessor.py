import cv2
import numpy as np
from deskew import determine_skew
from scipy import ndimage
import os
from customException import PreProcessorExceptions

BASE_PATH = 'processed_images/'
class PreProcessor:
  def __init__(self, path) -> None:
    self.originalImgPath = path
    self.imgName = self._extractFileName()
    self._readImage()
    self._normalize()
    self._skewCorrection()
    self._noiseRemoval()
    self._thinning()
    self._grayScale()
    self._thresholding()

  def cleanupFiles(self):
    my_dir = BASE_PATH
    for fname in os.listdir(my_dir):
      if self.imgName in fname:
        os.remove(os.path.join(my_dir, fname))

  def _readImage(self):
    img = cv2.imread(self.originalImgPath)
    self.img = cv2.flip(img, 1)
    if self.img is None:
      raise PreProcessorExceptions("unable to read image file")

  def _normalize(self):
    try:
      norm_img = np.zeros((self.img.shape[0], self.img.shape[1]))
      self.img = cv2.normalize(self.img, norm_img, 0, 255, cv2.NORM_MINMAX)
    except Exception as e:
      raise PreProcessorExceptions(e.args, "unable to normalize image")
    newPath = BASE_PATH + self.imgName + '_normalized.jpg'
    cv2.imwrite(newPath, self.img)
    self.normalizedImgPath = newPath

  def _skewCorrection(self):
    try:
      grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
      angle = determine_skew(grayscale)
      self.img = ndimage.rotate(self.img, angle)
    except Exception as e:
      raise PreProcessorExceptions(e.args, "unable to skewcorrect the image")
    newPath = BASE_PATH + self.imgName + '_skewCorrected.jpg'
    cv2.imwrite(newPath, self.img)
    self.skewCorrectedImgPath = newPath

  def _noiseRemoval(self):
    try:
      self.img = cv2.fastNlMeansDenoisingColored(self.img, None, 10, 10, 7, 15)
    except Exception as e:
      raise PreProcessorExceptions(e.args, "unable to remove noise of image")
    newPath = BASE_PATH + self.imgName + '_noiseRemoved.jpg'
    cv2.imwrite(newPath, self.img)
    self.noiseRemovedImgPath = newPath

  def _thinning(self):
    try:
      kernel = np.ones((2,2),np.uint8)
      self.img = cv2.erode(self.img, kernel, iterations = 1)
    except Exception as e:
      raise PreProcessorExceptions(e.args, "unable to thicken characters")
    newPath = BASE_PATH + self.imgName + '_eroded.jpg'
    cv2.imwrite(newPath, self.img)
    self.erodedImgPath = newPath

  def _grayScale(self):
    try:
      self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    except Exception as e:
      raise PreProcessorExceptions(e.args, "unable to change image to greyscale")
    newPath = BASE_PATH + self.imgName + '_grayScale.jpg'
    cv2.imwrite(newPath, self.img)
    self.grayScaleImgPath = newPath

  def _thresholding(self):
    try:
      self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    except Exception as e:
      raise PreProcessorExceptions(e.args, "unable to change img threshold")
    newPath = BASE_PATH + self.imgName + '_threshold.jpg'
    cv2.imwrite(newPath, self.img)
    self.thresholdImgPath = newPath

  def _extractFileName(self):
    return os.path.basename(self.originalImgPath).split('/')[-1].split('.')[0]


