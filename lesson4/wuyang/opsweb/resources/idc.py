from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse


class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        print(request.POST)

        print(reverse("success", kwargs={"next":"user_list"}))
        #return redirect("success", next="user_list")
        errmsg = "人为的失败，请重新处理"
        return redirect("error",next="idc_add",msg="人为的失败，请重新处理")
        #return HttpResponse("")