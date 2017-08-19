from django import template
from django.utils.html import format_html  # 引入format_html模块

register = template.Library()

# 计算template/user/userlist.html 传进来的current_page,p 参数
@register.simple_tag
def get_page(current_page,p):
	offset = abs(int(current_page) - int(p))
	# 取绝对值
	if offset < 8:
		if current_page == p:
			page_ele = '''<li class="active"><a href="?page=%s">%s</a></li>''' % (p,p)
		else:
			page_ele = '''<li><a href="?page=%s">%s</a></li>''' % (p,p)
		return format_html(page_ele)
	else:
		return ''