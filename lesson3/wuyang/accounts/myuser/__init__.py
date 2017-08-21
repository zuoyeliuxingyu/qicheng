#coding:utf-8

from django.contrib.auth.models import User

from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.http import JsonResponse

class UserListView(ListView):
    model = User
    template_name = "user/myuserlist.html"

    paginate_by = 8
    before_range_num = 7
    after_range_num = 6

    # 去除超级管理员用户
    def get_queryset(self):
        queryset = super(UserListView,self).get_queryset()
        queryset.filter(is_superuser=False)
        return  queryset
    # 分页数据方法重写
    def get_context_data(self, **kwargs):
        context = super(UserListView,self).get_context_data()
        page_obj = context['page_obj']
        context["page_range"]=self.get_page_range(page_obj)
        return context

    # 获取分页范围的方法
    def get_page_range(self,page_obj):
        current_index = page_obj.number
        temp_start_page = current_index - self.before_range_num
        temp_end_page = current_index + self.after_range_num

        if temp_start_page > 0:
            start_page = temp_start_page
        else:
            start_page = 1
            temp_end_page = start_page + self.before_range_num + self.after_range_num

        if temp_end_page < page_obj.paginator.num_pages:
            end_page = temp_end_page
        else:
            end_page=page_obj.paginator.num_pages
            temp_start_page=end_page-self.after_range_num-self.before_range_num
            if temp_start_page > 0:
                start_page = temp_start_page
            else:
                start_page = 1
        page_range=range(start_page,end_page)
        return page_range


class ModifyUserStatusView(View):
    def post(self,request,*agrs,**kwargs):
        ret={}
        uid = request.POST.get("uid")
        if uid:
            try:
                user = User.objects.get(id=uid)
                if user.is_active:
                    user.is_active = False
                else:
                    user.is_active = True
                user.save()
                ret["status"]=0
            except Exception as e:
                print(e)
                ret["status"]=1
                ret["errmsg"]="修改失败"
        else:
            ret["status"]=1
            ret["errmsg"]="请输入用户id"
        return JsonResponse(ret)




