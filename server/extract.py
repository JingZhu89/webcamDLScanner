import easyocr
import keras_ocr
from abc import ABC, abstractmethod
from preProcessor import PreProcessor

class OCR(ABC):
  def __init__(self, path) -> None:
    self.path = path

  @abstractmethod
  def extract(self):
    pass

class EasyOCR(OCR):
  MIN = -10
  MAX = 10
  def __init__(self, path) -> None:
    super().__init__(path)

  def extract(self):
      self._getRawData()
      return self._formatRawData()

  def _getRawData(self):
    reader = easyocr.Reader(['en'], gpu = True)
    self.rawData = reader.readtext(self.path, min_size = 1)

  def _formatRawData(self):
    result = []
    for tuple in self.rawData:
      data = {'coordinate': tuple[0], 'text': tuple[1], 'confidence':tuple[2]}
      result.append(data)
    return result


class KerasOCR(OCR):
  MIN = -8
  MAX = 10
  def __init__(self, path) -> None:
    super().__init__(path)

  def extract(self):
    self._getRawData()
    return self._formatRawData()

  def _getRawData(self):
    pipeline = keras_ocr.pipeline.Pipeline()
    self.rawData = pipeline.recognize([self.path])[0]

  def _formatRawData(self):
    result = []
    for tuple in self.rawData:
      data = {'coordinate': tuple[1][0], 'text': tuple[0], 'confidence': None}
      result.append(data)
    return result

pp = PreProcessor("test_images/MO.webp")
easy = EasyOCR(pp.grayScaleImgPath)
data = easy.extract()
for el in data : print(el)

