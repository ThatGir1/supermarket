from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'user/index.html')

def register(request):
    return render(request,'user/reg.html')

def login(request):
    return render(request,'user/login.html')