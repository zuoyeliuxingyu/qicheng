# coding=utf-8
from django import forms


class IdcForm(forms.Form):
    """验证 idc 输入的表单"""
    name = forms.CharField(required=True, max_length=10, error_messages={"required":"机房简称不能为空",
                                                                        "max_length":"长度必须小于10"})
    idc_name = forms.CharField(required=True, max_length=32)
    address = forms.CharField(required=True, max_length=255)
    phone = forms.CharField(required=True, max_length=20)
    email = forms.CharField(required=True, max_length=50)
    username = forms.CharField(required=True, max_length=32)

    # 自定义字段级别验证方法，方法名为【clean_<字段名>】
    def clean_name(self):
        # 将 name 字段强行变成小写
        name = self.cleaned_data.get('name')
        return name.lower()
