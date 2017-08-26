from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import Group, User


class UserLoginView(TemplateView):
    template_name = "public/login.html"

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        ret = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "username or passwrod fail, or user is not active"
        return JsonResponse(ret)

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))