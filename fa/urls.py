#-*-coding:utf-8-*-
#！usr/bin/env python
'''
Created on 2017年2月8日

@author: 武明辉
'''
from django.conf.urls import url

from fa import views

app_name='fa'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^mainpage/$',views.mainPage,name='mainpage'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^ajax_deal/$',views.ajax_deal,name='ajax_deal'),
    url(r'^exportexcel/$',views.exportitems,name='exportexcel'),
]

