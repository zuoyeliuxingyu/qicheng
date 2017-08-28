from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, JsonResponse
from resources.models import Idc

class ListIdcView(TemplateView):
    #model = Idc
    template_name = "list_idc.html"

    def get_context_data(self, **kwargs):
        context = super(ListIdcView, self).get_context_data(**kwargs)
        context["idc_obj"] = Idc.objects.all()
        print(Idc.objects.all())
        return context


class CreateIdcView(TemplateView):
    template_name = "add_idc.html"

    #def post(self, request):
        #print(request.POST)
        #print(reverse("success",kwargs={"next":"user_list"}))

        #return redirect("success",next="user_list")
        #errmsg = "人为的失败，请重新处理"
        #return redirect("error",next="idc_add",msg="人为的失败，请重新处理")
        #return HttpResponse("")

    def post(self, request):
        ret = {"status":0}
        name = request.POST.get("name","")
        cn_name = request.POST.get("idc_name","")
        addr = request.POST.get("address","")
        phone = request.POST.get("user_phone","")
        email = request.POST.get("mail","")
        username = request.POST.get("username","")
        idc_obj = Idc()
        try:
            idc_obj.name = name
            idc_obj.idc_name = cn_name
            idc_obj.address = addr
            idc_obj.phone = phone
            idc_obj.email = email
            idc_obj.username = username
            idc_obj.save()
        except:
            ret["status"] = 1
            ret["errmsg"] = "该机房已存在"
        #print(name,addr,phone,email,username)
        return JsonResponse(ret,safe=True)
