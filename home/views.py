from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
class VerifyViewMiddleware(View):

    @method_decorator(login_required(login_url='/admin/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserVerify(View):

    def get(self, request):

        return render(request, 'admin/login.html')

    def post(self, request):
        val_verify = LoginForm(request.POST)
        if val_verify.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            result = authenticate(username=user_name, password=pass_word)
            if result is None:
                res = {
                    "error_msg": "账号或密码错误"
                }
            else:
                if result.is_active:
                    login(request, result)
                    res = {
                        "error_msg": "",
                        "code": "0"
                    }
                else:
                    res = {
                        "error_msg": "用户未激活"
                    }
        else:
            err_str = ""
            for k, v in val_verify.errors.as_data().items():
                err_str = k + ": " + str(v[0].message)
                break
            res = {
                "error_msg": err_str,
                "code": "001",
                "data": []
            }

        return JsonResponse(res)


class IndexView(VerifyViewMiddleware):

    def get(self, request):

        return render(request, 'admin/index.html')

    def post(self, request):
        pass
