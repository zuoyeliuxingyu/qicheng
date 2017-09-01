# coding:utf8
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from resources.models import Idc

class IdcListView(LoginRequiredMixin, ListView):
    template_name = "idc/idclist.html"
    model = Idc
    ordering = "id"

    def get_queryset(self):
        queryset = super(IdcListView, self).get_queryset()  # 存放列表对象(对应表里数据的集合)
        idcname = self.request.GET.get("search_idcname","")
        if idcname:
            queryset = queryset.filter(name__icontains=idcname)
        return queryset

class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):

        #print(request.POST)
        #print(reverse("success",kwargs={"next":"user_list"}))
        #return redirect("success", next="user_list")
        #return redirect("error",next="idc_add", msg="Please resubmit!!!")

        ret = {}
        data = {}
        for k in request.POST:
            data[k] = request.POST.get(k,"")
        data.pop("csrfmiddlewaretoken")
        #print(data)
        try:
            idc = Idc(**data)
            idc.save()
            return redirect("success", next="idc_list")
        except:
            ret["msg"] = "Idc already exists or other errors"
            return redirect("error",next="idc_add", msg=ret["msg"])
