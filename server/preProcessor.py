import cv2
import numpy as np
from deskew import determine_skew
from scipy import ndimage
from skimage import exposure
from PIL import Image
import os
from customException import PreProcessorExceptions

BASE_PATH = 'processed_images/'


class PreProcessor:
    def __init__(self, path, type) -> None:
        self.originalImgPath = path
        self.type = type
        self.imgName = self._extractFileName()
        self._readImage()
        self._flipImage()
        self._normalize()
        self._skewCorrection()
        self.__reduceBlurry()
        # self._noiseRemoval()
        self._thinning()
        self._grayScale()
        self._thresholding()

    def cleanupFiles(self):
        my_dir = BASE_PATH
        for fname in os.listdir(my_dir):
            if self.imgName in fname:
                os.remove(os.path.join(my_dir, fname))

    def _readImage(self):
        self.img = cv2.imread(self.originalImgPath)
        if self.img is None:
            raise PreProcessorExceptions(
                additionalMsg="unable to read image file")

    def _flipImage(self):
        if self.type == 'webcam':
            self.img = cv2.flip(self.img, 1)
            newPath = BASE_PATH + self.imgName + '_flippedImg.jpg'
            cv2.imwrite(newPath, self.img)
            self.flippedImgPath = newPath

    def __reduceBlurry(self):
        p2, p98 = np.percentile(self.img, (2, 98))
        enhanced_image = exposure.rescale_intensity(
            self.img, in_range=(p2, p98))
        blurred_image = cv2.GaussianBlur(enhanced_image, (5, 5), 0)
        self.img = cv2.addWeighted(enhanced_image, 1.5, blurred_image, -0.5, 0)
        newPath = BASE_PATH + self.imgName + '_reduceBlurry.jpg'
        cv2.imwrite(newPath, self.img)
        self.reduceBlurryImgPath = newPath

    def _normalize(self):
        try:
            norm_img = np.zeros((self.img.shape[0], self.img.shape[1]))
            self.img = cv2.normalize(
                self.img, norm_img, 0, 255, cv2.NORM_MINMAX)
        except Exception as e:
            raise PreProcessorExceptions(
                additionalMsg="unable to normalize image")
        newPath = BASE_PATH + self.imgName + '_normalized.jpg'
        cv2.imwrite(newPath, self.img)
        self.normalizedImgPath = newPath

    def _skewCorrection(self):
        try:
            grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            angle = determine_skew(grayscale)
            self.img = ndimage.rotate(self.img, angle, axes=(0, 1))
        except Exception as e:
            raise PreProcessorExceptions(
                additionalMsg="unable to skewcorrect the image")
        newPath = BASE_PATH + self.imgName + '_skewCorrected.jpg'
        cv2.imwrite(newPath, self.img)
        self.skewCorrectedImgPath = newPath

    def _noiseRemoval(self):
        try:
            self.img = cv2.fastNlMeansDenoisingColored(
                self.img, None, 10, 10, 7, 15)
        except Exception as e:
            raise PreProcessorExceptions(
                additionalMsg="unable to remove noise of image")
        newPath = BASE_PATH + self.imgName + '_noiseRemoved.jpg'
        cv2.imwrite(newPath, self.img)
        self.noiseRemovedImgPath = newPath

    def _thinning(self):
        try:
            kernel = np.ones((2, 2), np.uint8)
            self.img = cv2.erode(self.img, kernel, iterations=1)
        except Exception as e:
            raise PreProcessorExceptions(
                additionalMsg="unable to thicken characters")
        newPath = BASE_PATH + self.imgName + '_eroded.jpg'
        cv2.imwrite(newPath, self.img)
        self.erodedImgPath = newPath

    def _grayScale(self):
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            raise PreProcessorExceptions(
                additionalMsg="unable to change image to greyscale")
        newPath = BASE_PATH + self.imgName + '_grayScale.jpg'
        cv2.imwrite(newPath, self.img)
        self.grayScaleImgPath = newPath

    def _thresholding(self):
        try:
            self.img = cv2.threshold(
                self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        except Exception as e:
            raise PreProcessorExceptions(
                additionalMsg="unable to change img threshold")
        newPath = BASE_PATH + self.imgName + '_threshold.jpg'
        cv2.imwrite(newPath, self.img)
        self.thresholdImgPath = newPath

    def _extractFileName(self):
        return os.path.basename(self.originalImgPath).split('/')[-1].split('.')[0]
