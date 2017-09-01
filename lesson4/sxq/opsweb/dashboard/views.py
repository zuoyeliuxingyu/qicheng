from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def index(request):
    #data_dict = {'name':'reboot'}
    #data_list = ['a', 'b', 'c']
    #return HttpResponse('<p>hello world</p>') 
    #return JsonResponse(data_list, safe=False)
    #return JsonResponse(data_dict)

    # get_template
    #t = loader.get_template('test.html')
    #context = {"name":"xxxxx"}
    #return HttpResponse(t.render(context, request))

    # render
    #context = {"name":"xxxxx"}
    #return render(request,"test.html",context)
   
    #if request.method == "POST":
    #    print(request.POST)
    #    user = request.POST.get('username', "")
    #    passwd = request.POST.get('userpass', "")
    #    if user == 'admin' and passwd == 'admin':
    #        return HttpResponse('Login Success!!!')
    #    else:
    #        return HttpResponse('Login Fails!!!')
    #else:
    return render(request, 'index.html') 

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

#def user_detail(request,*args, **kwargs):
#    print(args)
#    print(kwargs)
#    return HttpResponse('ok')

class SuccessView(TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
         context = super(SuccessView, self).get_context_data(**kwargs)
         #print(self.kwargs)
         success_name = self.kwargs.get("next", "")
         #print(success_name)

         next_url = "/"
         try:
            next_url = reverse(success_name) 
         except:
            pass 
         context["next_url"] = next_url
         return context

class ErrorView(TemplateView):
    template_name = "public/error.html"

    def get_context_data(self, **kwargs):
         context = super(ErrorView, self).get_context_data(**kwargs)
         error_name = self.kwargs.get("next", "")
         errmsg = self.kwargs.get("msg", "")
         next_url = "/"
         try:
            next_url = reverse(error_name)
         except:
            pass
         context["next_url"] = next_url
         context["errmsg"] = errmsg
         return context
