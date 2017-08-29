from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from resources.models import Idc
from django.db import IntegrityError
from django.http import JsonResponse

class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        try:
            data = {
                "name": request.POST.get("name", ""),
                "idc_name": request.POST.get("idc_name", ""),
                "address": request.POST.get("address", ""),
                "phone": request.POST.get("phone", ""),
                "email": request.POST.get("email", ""),
                "username": request.POST.get("username", "")
            }
            Idc.objects.create(**data)
        except IntegrityError:
            return redirect("error", next="idc_add", msg="idc名称已创建，请重新输入")
        return redirect("success", next="idc_list")

class IdcViewList(View):
    '''
    IDC列表
    '''
    def get(self, request, *args, **kwargs):
        idc_queryset = Idc.objects.all()
        return render(request, "idc/idc_list.html", {"idclist": idc_queryset})
