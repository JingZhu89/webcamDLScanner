import easyocr
import keras_ocr
from abc import ABC, abstractmethod

class OCR(ABC):
  def __init__(self, path) -> None:
    self.path = path

  @abstractmethod
  def extract(self):
    pass

class EasyOCR(OCR):
  MIN = -8
  MAX = 10
  def __init__(self, path) -> None:
    super().__init__(path)

  def extract(self):
    result = []
    reader = easyocr.Reader(['en'], gpu = True)
    extracted_info = reader.readtext(self.path, min_size = 1)
    for tuple in extracted_info:
      data = {'coordinate': tuple[0], 'text': tuple[1], 'confidence':tuple[2]}
      result.append(data)
    return result

class KerasOCR(OCR):
  MIN = -8
  MAX = 10
  def __init__(self, path) -> None:
    super().__init__(path)

  def extract(self):
    result = []
    pipeline = keras_ocr.pipeline.Pipeline()
    extracted_info = pipeline.recognize([self.path])
    for tuple in extracted_info[0]:
      data = {'coordinate': tuple[1], 'text': tuple[0], 'confidence': None}
      result.append(data)
    return result





