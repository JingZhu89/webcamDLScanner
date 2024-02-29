from asyncio import constants
from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin
from extract import EasyOCR, KerasOCR
from preProcessor import PreProcessor
from parseText import ParseText
import base64
from PIL import Image
import os
from customException import TextParserExceptions, PreProcessorExceptions
TEMP_IMG_LOCATION = "test_images/temp_decoded.jpeg"

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/webcam', methods=['POST'])
@cross_origin(supports_credentials=True)
def processWebcamDL():
  try:
    data = request.get_json()
    img = data['img']
    decodeBase64Img(img)
    returnedData = processData('webcam')
    cleanUpImg()
  except Exception as e:
    if isinstance(e, TextParserExceptions) or isinstance(e, PreProcessorExceptions):
      return {'error': e.addtionalMsg}, 400
    else:
      return {'error': e.args}, 500
  return returnedData

@app.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def processUploadDL():
  try:
    img = request.files['img']
    Image.open(img).save(TEMP_IMG_LOCATION)
    returnedData = processData('upload')
    cleanUpImg()
  except Exception as e:
    if isinstance(e, TextParserExceptions) or isinstance(e, PreProcessorExceptions):
      return {'error': e.addtionalMsg}, 400
    else:
      return {'error': e.args}, 500
  return returnedData

def decodeBase64Img(img):
  base64ImgStr = str(img)
  trimmedImgStr = base64ImgStr[base64ImgStr.find(",")+1:]
  image = base64.urlsafe_b64decode(trimmedImgStr)
  file_to_save = TEMP_IMG_LOCATION
  with open(file_to_save, "wb") as f:
    f.write(image)

def cleanUpImg():
  os.remove(TEMP_IMG_LOCATION)

def processData(type):
  myPorcessor = PreProcessor('test_images/temp_decoded.jpeg', type)
  easy = EasyOCR(myPorcessor.grayScaleImgPath)
  parse = ParseText(easy.extract())
  myPorcessor.cleanupFiles()
  returnData =  parse.parseData()
  return returnData
