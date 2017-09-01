#!/usr/bin/python
# coding=utf8

from django.views.generic import View, TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from resources.models import Idc

# class CreateIdcView(TemplateView):

#     template_name = "add_idc.html"

#     def post(self, request):
#         print(request.POST)
#         print(reverse("success", kwargs={"next": "user_lsit"}))
#         # return redirect("suceess", next="user_list")
#         return redirect("error", next="idc_add", msg="人为失败")
        # return HttpResponse("")

class IdcListView(ListView):
    """IDC 信息展示逻辑"""

    template_name = "idclist.html"
    model = Idc


class AddIdcView(TemplateView):
    """增加 IDC 逻辑"""
    template_name = "add_idc.html"

    def post(self, request):
        # forms = IdcForm(request.POST)
        # print(forms)      # 取表单数据，是一个dict
        data = {
            "name": request.POST.get('name', ''),
            "idc_name": request.POST.get('idc_name', ''),
            "address": request.POST.get('address', ''),
            "phone": request.POST.get('user_phone', ''),
            "email": request.POST.get('mail', ''),
            "username": request.POST.get('username', '')
        }

        try:
            idc = Idc(**data)
            idc.save()
        except Exception as e:
            return redirect(reverse("idc_add"))

        return redirect(reverse("idc_list"))


class DeleteIdcView(View):
    """删除 Idc 的逻辑，响应前端 ajax 请求"""
    def post(self, request):
        ret = {'status': 0}
        idc_id = request.POST.get('idc_id', '')     # 获取前端 ajax 传递过来的 idc_id

        # 获取 idc_id 后进行对应的删除，异常给予报错提示
        try:
            idc = Idc.objects.get(id=idc_id)
            idc.delete()
        except Idc.DoesNotExist:
            ret['stauts'] = 1
            ret['errmsg'] = "Idc不存在"

        return JsonResponse(ret)
