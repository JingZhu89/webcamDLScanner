from django.shortcuts import render
from django.http import HttpResponse

from myapp.extract import EasyOCR, KerasOCR
from myapp.preProcessor import PreProcessor
from myapp.parseText import ParseText

# Create your views here.
def home(request):
  print(request.read(), request.path, request.method)
  return HttpResponse("Hello, world. You're at the polls index.")
