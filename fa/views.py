#-*-coding:utf-8-*-
import StringIO

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import xlwt

from FAIS import settings
from fa.models import EquipmentBasticInfo, EquipmentType


# Create your views here.
def index(request):
    context={'error':request.GET.get('message')}
    return render(request, 'fa/index.html', context)

def login(request):
    #在这里写登录逻辑、即登陆成功怎么样不成功怎么样子
    nid=request.POST['nid']
    password=request.POST['password']
    user=auth.authenticate(username=nid,password=password)
    if user  is  None:#处理空用户名和密码有错误逻辑
        return HttpResponseRedirect('/fa?message=verify_error')
    else:
        if user.is_active:#登陆
            auth.login(request,user)
            return HttpResponseRedirect('/fa/mainpage')
        else:
            return HttpResponseRedirect('/fa?message=verify_exception')

def logout(request):
    user=request.user
    if user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/fa')

@login_required(login_url=settings.LOGIN_URL)
def mainPage(request):
   
    context={'user':request.user,}
    return render(request, 'fa/mainpage.html', context)

@login_required(login_url=settings.LOGIN_URL)
def equipmentm(request):
    info=EquipmentBasticInfo.objects.all()
    clzzs=EquipmentType.objects.all()
    context={'info':info,'clzzs':clzzs}
    return render(request, 'fa/equipmentm.html', context)

@login_required(login_url=settings.LOGIN_URL)
def exportitems(request):
    '''
            导出数据到excel表格
    '''
    
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=export.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'Sheet1')
    #第一行表头  
    sheet.write(0,0, '经销商编码')
    sheet.write(0,1, '经销商名称')
    sheet.write(0,2, '终端医院编码')
    sheet.write(0,3, '终端医院名称')
   
    row = 1
    for item in EquipmentBasticInfo.objects.all():
        sheet.write(row,0, item.name)
        sheet.write(row,1, item.name)
        sheet.write(row,2, item.name)
        sheet.write(row,3, item.name)
        row=row + 1
       
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response
    
