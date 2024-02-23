from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myapp.extract import EasyOCR, KerasOCR
from myapp.preProcessor import PreProcessor
from myapp.parseText import ParseText
from io import BytesIO
from PIL import Image
import base64

# Create your views here.
def home(request):
  if request.method == 'POST':
    data = request.body
    # bytes_decoded = base64.b64decode(data)
    # img = Image.open(BytesIO(bytes_decoded))
    # out_jpg = img.convert('RGB')
    # out_jpg.save('test_images/me.jpg')
    myPorcessor = PreProcessor('myapp/test_images/missouri.webp')
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

  return JsonResponse(data)
