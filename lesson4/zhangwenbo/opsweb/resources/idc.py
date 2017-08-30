from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from resources.models import Idc
from django.db import IntegrityError
from django.http import JsonResponse, QueryDict

class CreateIdcView(TemplateView):
    """
    创建IDC
    """
    template_name = "idc/add_idc.html"

    def post(self, request):
        name = request.POST.get("name", "")
        if name:
            try:
                data = {
                    "name": name,
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
        return redirect("error", next="idc_add", msg="idc名称没输入，请重新输入")

class IdcViewList(View):
    '''
    IDC列表
    '''
    def get(self, request, *args, **kwargs):
        idc_queryset = Idc.objects.all()
        return render(request, "idc/idc_list.html", {"idclist": idc_queryset})

class IdcDelete(View):
    """
    删除IDC
    """
    def delete(self, request):
        ret = {"status":0}
        data = QueryDict(request.body)
        idc_id = data.get("idcid", "")
        try:
            Idc.objects.filter(id=idc_id).delete()
        except Idc.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "该idc不存在"
            return JsonResponse(ret)
        return  JsonResponse(ret)