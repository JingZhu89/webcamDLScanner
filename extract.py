import easyocr
# from paddleocr import PaddleOCR, draw_ocr
# ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
# img_path = './imgs/11.jpg'
# result = ocr.ocr(img_path, cls=True)
# for idx in range(len(result)):
#     res = result[idx]
#     for line in res:
#         print(line)

# reader = easyocr.Reader(['en'], gpu = True)

class Easyocr:
  def __init__(self, path) -> None:
      self.path = path

  def extract(self):
    reader = easyocr.Reader(['en'], gpu = True)
    return reader.readtext(self.path, min_size = 1)

easy = Easyocr('test_images/missouri.webp')
print(easy.extract())