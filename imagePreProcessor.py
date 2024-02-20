from locale import normalize
import cv2
import numpy as np

class PreProcessor:
  def __init__(self, path) -> None:
    self.img = cv2.imread(path)
    self.normalize()
    self.skewCorrection()
    self.noiseRemoval()
    self.grayScale()
    self.thresholding()

  def normalize(self):
    norm_img = np.zeros((self.img.shape[0], self.img.shape[1]))
    self.img = cv2.normalize(self.img, norm_img, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("normalized.jpg", self.img)

  def skewCorrection(self):
    co_ords = np.column_stack(np.where(self.img > 0))
    angle = cv2.minAreaRect(co_ords)[-1]
    if angle < -45:
      angle = -(90 + angle)
    else:
      angle = -angle
    (h, w) = self.img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(self.img, M, (w, h), flags=cv2.INTER_CUBIC,
    borderMode=cv2.BORDER_REPLICATE)
    self.img = rotated
    cv2.imwrite("skewCorrected.jpg", self.img)

  def noiseRemoval(self):
    self.img = cv2.fastNlMeansDenoisingColored(self.img, None, 10, 10, 7, 15)
    cv2.imwrite("moiseRemoved.jpg", self.img)

  def grayScale(self):
    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("grayScale.jpg", self.img)

  def thresholding(self):
    self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite("threshold.jpg", self.img)

img = PreProcessor('test_images/missouri.webp')