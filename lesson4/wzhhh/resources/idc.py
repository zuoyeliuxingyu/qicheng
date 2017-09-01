from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from resources.models import Idc

class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        print(request.POST)
        print(reverse("success", kwargs={"next": "user_list"}))

        data = Idc()
        data.name = request.POST.get("name", "")
        data.idc_name = request.POST.get("idc_name", "")
        data.address = request.POST.get("address", "")
        data.username = request.POST.get("username", "")
        data.phone = request.POST.get("phone", "")
        data.email = request.POST.get("email", "")

        try:
            data.save()
            return redirect("success", next="idc_list")
        except:
            errmsg = "人为失败"
            return redirect("error", next="idc_add", msg=errmsg)
        #return HttpResponse("")


class IdcListView(ListView):
    template_name = "idc/idc_list.html"
    model = Idc