from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

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

class IndexView(TemplateView):

    template_name = "index.html"
    
    @method_decorator(login_required) 
    def get(self,request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

#def user_detail(request,*args, **kwargs):
#    print(args)
#    print(kwargs)
#    return HttpResponse('ok')
