from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin
from extract import EasyOCR, KerasOCR
from preProcessor import PreProcessor
from parseText import ParseText
import base64, binascii

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def processDL():
  if request.method == 'POST':
    base64ImgStr = str(request.data)
    trimmedImgStr = base64ImgStr[base64ImgStr.find(",")+1:]
    try:
      # file_to_save = "test_images/temp_original.jpeg"
      # with open(file_to_save, "wb") as f:
      #   f.write(base64ImgStr.)
      image = base64.urlsafe_b64decode(trimmedImgStr)
      file_to_save = "test_images/temp_decoded.jpeg"
      with open(file_to_save, "wb") as f:
        f.write(image)
    except binascii.Error as e:
      print(e)
    myPorcessor = PreProcessor('test_images/temp_decoded.jpeg')
    easy = EasyOCR(myPorcessor.grayScaleImgPath)
    parse = ParseText(easy.MIN, easy.MAX, easy.extract())
    data =  parse.parseData()
    # myPorcessor.cleanupFiles()
    print(data)
    return data
