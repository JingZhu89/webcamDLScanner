from flask import Flask, request, redirect

from flask_cors import CORS
from extract import EasyOCR, KerasOCR
from preProcessor import PreProcessor
from parseText import ParseText

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST', 'GET'])
def processDL():
  if request.method == 'POST':
    # bytes_decoded = base64.b64decode(data)
    # img = Image.open(BytesIO(bytes_decoded))
    # out_jpg = img.convert('RGB')
    # out_jpg.save('test_images/me.jpg')
    myPorcessor = PreProcessor('test_images/missouri.webp')
    easy = EasyOCR(myPorcessor.grayScaleImgPath)
    extractedData = ParseText(easy.MIN, easy.MAX, easy.extract())
    data =  {
              'first_name': extractedData.firstName,
              'last_name': extractedData.lastName,
              'address': extractedData.addressOne + ' ' + extractedData.addressTwo,
              'issue_date': extractedData.issueDate,
              'expiration_date': extractedData.expirationDate
            }
    print(data)
    myPorcessor.cleanupFiles()
    return data