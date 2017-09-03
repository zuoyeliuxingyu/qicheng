#!/usr/bin/python
# coding=utf8

from django.views.generic import View, TemplateView, ListView
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from resources.models import Idc
from django.core import serializers

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

        errmsg = []
        if not name:
            errmsg.append("idc 简称不能为空")
        if not idc_name:
            errmsg.append("idc 名称不能为空")
        if errmsg:
            return redirect("error", next="idc_add", msg=json.dumps(errmsg))

        try:
            idc = Idc(**data)
            idc.save()
        except Exception as e:
            # return redirect(reverse("idc_add"))
            return redirect("error", next="idc_add", msg=e.args)
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


class IdcMoreView(View):
    """IDC 详情按钮的逻辑，响应后端的需求"""
    def get(self, request):
        idc_id = request.GET.get('idc_id', '')
        # print(idc_id)
        try:
            idc = Idc.objects.get(id=idc_id)
        except Idc.DoesNotExist:
            return JsonResponse([], safe=False)

        # print(idc.__dict__)
        # 为了排除上述 dict 的非可用 "_state" key
        new_idc_obj = {}
        for i in idc.__dict__:
            if i != "_state":
                new_idc_obj[i] = idc.__dict__[i]
        # print(new_idc_obj)
        return JsonResponse(new_idc_obj)
        # return HttpResponse(serializers.serialize("json", idc_obj.__dict__), content_type="application/json")
        # return render(request, {"idc_obj": idc_obj})
        # return HttpResponse("")
