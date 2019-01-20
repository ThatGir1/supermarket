from django.shortcuts import render

# Create your views here.
from django.views import View


class RegisterView(View):
    def get(self,request):
        return render(request,'user/reg.html')

    def post(self,request):
        pass

class LoginView(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        pass
