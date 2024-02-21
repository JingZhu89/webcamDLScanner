from curses import newpad
import cv2
import numpy as np
from deskew import determine_skew
from scipy import ndimage
import os

class PreProcessor:
  def __init__(self, path) -> None:
    self.originalImgPath = path
    self.imgName = self.extractFileName()
    self.img = cv2.imread(path)
    self.normalize()
    self.skewCorrection()
    self.noiseRemoval()
    self.thinning()
    self.grayScale()
    self.thresholding()

  def normalize(self):
    norm_img = np.zeros((self.img.shape[0], self.img.shape[1]))
    self.img = cv2.normalize(self.img, norm_img, 0, 255, cv2.NORM_MINMAX)
    newPath = 'processed_images/' + self.imgName + '_normalized.jpg'
    cv2.imwrite(newPath, self.img)
    self.normalizedImgPath = newPath

  def skewCorrection(self):
    grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(grayscale)
    self.img = ndimage.rotate(self.img, angle)
    newPath = 'processed_images/' + self.imgName + '_skewCorrected.jpg'
    cv2.imwrite(newPath, self.img)
    self.skewCorrectedImgPath = newPath

  def noiseRemoval(self):
    self.img = cv2.fastNlMeansDenoisingColored(self.img, None, 10, 10, 7, 15)
    newPath = 'processed_images/' + self.imgName + '_noiseRemoved.jpg'
    cv2.imwrite(newPath, self.img)
    self.noiseRemovedImgPath = newPath

  def thinning(self):
    kernel = np.ones((2,2),np.uint8)
    self.img = cv2.erode(self.img, kernel, iterations = 1)
    newPath = 'processed_images/' + self.imgName + '_eroded.jpg'
    cv2.imwrite(newPath, self.img)
    self.erodedImgPath = newPath

  def grayScale(self):
    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    newPath = 'processed_images/' + self.imgName + '_grayScale.jpg'
    cv2.imwrite(newPath, self.img)
    self.grayScaleImgPath = newPath

  def thresholding(self):
    self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    newPath = 'processed_images/' + self.imgName + '_threshold.jpg'
    cv2.imwrite(newPath, self.img)
    self.thresholdImgPath = newPath

  def extractFileName(self):
    return os.path.basename(self.originalImgPath).split('/')[-1].split('.')[0]