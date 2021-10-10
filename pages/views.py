from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):
    return render(request,'pages/index.html')
