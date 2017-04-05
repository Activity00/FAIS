#-*-coding:utf-8-*-
#!usr/bin/env python
'''
Created on 2017年3月23日

@author: 武明辉
'''

from django import forms
from django.contrib.admin import widgets
from django.forms.models import ModelForm

from fa.models import EquipmentBasticInfo, EquipmentType, EquipmentPosition


# class BaseinfoForm(forms.Form):
#     name=forms.CharField(label='设备名称',max_length=50)
# class BaseinfoForm(ModelForm):
#     
#     class Meta:
#         model=EquipmentBasticInfo
#         fields='__all__'
class BaseinfoForm(forms.Form):
    name=forms.CharField(required=True,label='设备名称') 
    type=forms.ModelChoiceField(queryset=EquipmentType.objects.all(),label='设备类型')
    modelType=forms.CharField(required=True,label='设备型号')
    price=forms.IntegerField(required=True,label='设备单价')
    user=forms.CharField(required=True,label='使用人')
    position=forms.ModelChoiceField(EquipmentPosition.objects.all(),label='设备新型号')
    purchasetime=forms.DateTimeField(widget=widgets.AdminDateWidget(),label='购买时间')
    remark=forms.CharField(required=True,label='备注')
   
    
    
    
    