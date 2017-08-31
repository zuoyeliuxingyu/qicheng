from django.views.generic import TemplateView,ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse,QueryDict,JsonResponse
from resources.models import Idc
from django.db import IntegrityError

class CreateIdcView(TemplateView):
    template_name = "idc/add_idc.html"

    """
    添加idc的逻辑 先取出前端传过来信息的值 name，idc_name...然后定义一个字典 实例化models的Idc idc = Idc(**data)
    IntegrityError 是Django数据库的异常(id不能重复)
    做作业的时候发现添加idc页面里email 和 机房联系人怎么添加都是空 需要修改add_idc.html里的email 和 user_phone
    
    idc_obj = Idc()    添加idc的2种方式
    idc_obj.name = request.POST.get("name",None)
    idc_obj.idc_name = request.POST.get("idc_name",None)
    idc_obj.address = request.POST.get("address",None)
    idc_obj.phone = request.POST.get("phone",None)
    idc_obj.email = request.POST.get("email",None)
    idc_obj.username = request.POST.get("username",None)
    print(request.POST.get("phone"),request.POST.get("email"))
    idc_obj.save()
    """

    def post(self, request):
        print(request.POST)
        try:
            data = {
                "name":request.POST.get("name",""),
                "idc_name":request.POST.get("idc_name",""),
                "address":request.POST.get("address",""),
                "phone":request.POST.get("phone",""),
                "email":request.POST.get("email",""),
                "username":request.POST.get("username",""),
            }
            print(data)
            idc = Idc(**data)
            idc.save()
        except IntegrityError:
            return redirect("error",next="idc_add",msg="idc name已存在")
        return redirect("success", next="idc_list")
        #print(reverse("success", kwargs={"next":"user_list"}))
        #return redirect("success", next="user_list")
        errmsg = "人为的失败，请重新处理"
        #return redirect("error",next="idc_add",msg="人为的失败，请重新处理")
        #return HttpResponse("")

class ListIdcView(ListView):

    model = Idc
    template_name = "idc/idc_list.html"
    """
    在idc_list.html页面中有删除idc的button 这里处理的是删除idc的逻辑 delete方法是要从QueryDict里取出data数据 然后实例化idc的object 进行删除
    """
    def delete(self,request):
        ret = {"status":0}
        #print(QueryDict(request.body))
        data = QueryDict(request.body)
        idc_obj = Idc.objects.get(id=data.get('id',''))
        idc_obj.delete()
        return  JsonResponse(ret)