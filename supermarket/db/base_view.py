from django.utils.decorators import method_decorator
from django.views import View

from user.helper import check_login


class VerifyLoginView(View):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)