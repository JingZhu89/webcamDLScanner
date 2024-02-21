import cv2
import numpy as np
from deskew import determine_skew
from scipy import ndimage
import math

class PreProcessor:
  def __init__(self, path) -> None:
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
    # cv2.imwrite("normalized.jpg", self.img)

  # def skewCorrection(self):
  #   co_ords = np.column_stack(np.where(self.img > 0))
  #   print(co_ords)
  #   angle = cv2.minAreaRect(co_ords)[-1]
  #   if angle < -45:
  #     angle = -(90 + angle)
  #   else:
  #     angle = -angle
  #   (h, w) = self.img.shape[:2]
  #   center = (w // 2, h // 2)
  #   M = cv2.getRotationMatrix2D(center, angle, 1.0)
  #   rotated = cv2.warpAffine(self.img, M, (w, h), flags=cv2.INTER_CUBIC,
  #   borderMode=cv2.BORDER_REPLICATE)
  #   self.img = rotated
  #   cv2.imwrite("skewCorrected.jpg", self.img)

  def skewCorrection(self):
    grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(grayscale)
    self.img = ndimage.rotate(self.img, angle)
    # cv2.imwrite('skewCorrected.jpg', self.img)

  def noiseRemoval(self):
    self.img = cv2.fastNlMeansDenoisingColored(self.img, None, 10, 10, 7, 15)
    # cv2.imwrite("noiseRemoved.jpg", self.img)

  def thinning(self):
    kernel = np.ones((2,2),np.uint8)
    self.img = cv2.erode(self.img, kernel, iterations = 1)
    # cv2.imwrite("erosion.jpg", self.img)

  def grayScale(self):
    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("grayScale.jpg", self.img)

  def thresholding(self):
    self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite("threshold.jpg", self.img)

# def rotate(
#         image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
# ) -> np.ndarray:
#     old_width, old_height = image.shape[:2]
#     angle_radian = math.radians(angle)
#     width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
#     height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)
#     image_center = tuple(np.array(image.shape[1::-1]) / 2)
#     rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
#     rot_mat[1, 2] += (width - old_width) / 2
#     rot_mat[0, 2] += (height - old_height) / 2
#     return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

img = PreProcessor('test_images/missouri.webp')