from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myapp.extract import EasyOCR, KerasOCR
from myapp.preProcessor import PreProcessor
from myapp.parseText import ParseText

# Create your views here.
def home(request):
  print(request.read(), request.path, request.method)
  if request.method == 'GET':
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
    myPorcessor.cleanupFiles()
  return JsonResponse(data)
