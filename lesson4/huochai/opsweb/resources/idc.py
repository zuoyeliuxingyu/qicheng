from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from resources.models import Idc
from django.db import IntegrityError

# IDC添加
class CreateIdcView(TemplateView):
    template_name = 'idc/add_idc.html'

    def post(self, request):
        print(request.POST)
        idcinfo = request.POST.copy()
        idcinfo.pop('csrfmiddlewaretoken')
        idcdata = idcinfo.dict()
        idc = Idc(**idcdata)
        try:
            idc.save()
        except IntegrityError:
            return redirect('error', next='idc_add', errmsg='主键冲突')

        #print(reverse('success', kwargs={'next':'user_list'}))
        return redirect('success', next='user_list')
        #return HttpResponse('')

# IDC列表页面
class ListIdcView(TemplateView):
    template_name = 'idc/list_idc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idc = Idc.objects.values()
        context['idc'] = idc
        return context
