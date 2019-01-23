from django.shortcuts import render

# Create your views here.
from db.base_view import VerifyLoginView


class IndexView(VerifyLoginView):
    def get(self,request):
        return render(request,'goods/index.html')

    def post(self,request):
        pass

class DetailView(VerifyLoginView):
    def get(self,request):
        return render(request,'goods/detail.html')

    def post(self,request):
        pass


class ListView(VerifyLoginView):
    def get(self,request):
        return render(request,'goods/list.html')


    def post(self,request):
        pass

