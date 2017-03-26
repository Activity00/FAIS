#-*-coding:utf-8-*-
#！usr/bin/env python
'''
Created on 2017年3月23日

@author: 武明辉
'''
from django import forms
from django.forms.models import ModelForm

from fa.models import EquipmentBasticInfo


# class BaseinfoForm(forms.Form):
#     name=forms.CharField(label='设备名称',max_length=50)

class BaseinfoForm(ModelForm):
    class Meta:
        model=EquipmentBasticInfo
        fields='__all__'
    
    
    
    