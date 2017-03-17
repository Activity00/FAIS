#-*-coding:utf-8-*-
import StringIO
import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import xlwt

from FAIS import settings
from fa.models import EquipmentBasticInfo, EquipmentType, EquipmentPosition


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
def ajax_deal(request):
    '''左侧菜单栏点击事件处理'''
    req=request.GET.get('req')
    context={}
    if req=='sbgl':
        context=_sbgl(request)
    elif req=='wlzt':
        context=_wlzt(request)
    elif req=='bxgl':
        context=_bxgl(request)
    elif req=='ptsjtj':
        context=_ptsjtj(request)
    elif req=='grzl':
        context=_grzl(request)
    elif req=='xgmm':
        context=_xgmm(request)
        
    return render(request,'fa/%s.html'%req,context)

@csrf_exempt
@login_required(login_url=settings.LOGIN_URL)
def deletebaseinfo(request):
    '''删除基本信息操作'''
    jsonstr=json.loads(request.body)
    data=jsonstr['data']
    EquipmentBasticInfo.objects.filter(id__in=data).delete()
    return HttpResponse(json.dumps('200'),content_type="application/json")

@login_required(login_url=settings.LOGIN_URL)
def exportitems(request):
    '''
            导出数据到excel表格
    '''
    info=None
    type_id=request.GET.get('type_id')
    position_id=request.GET.get('position_id')
    if not type_id:
        type_id=0
    if not position_id:
        position_id=0
    type_id=int(type_id)
    position_id=int(position_id)
    if position_id==0 and type_id==0:
        info=EquipmentBasticInfo.objects.all()
    elif position_id==0 and type_id!=0:
        info=EquipmentBasticInfo.objects.filter(type=EquipmentType.objects.get(id=type_id))
    elif type_id==0 and position_id!=0:
        info=EquipmentBasticInfo.objects.filter(position=EquipmentPosition.objects.get(id=position_id))
    else:
        info=EquipmentBasticInfo.objects.filter(type=EquipmentType.objects.get(id=type_id),
                                                position=EquipmentPosition.objects.get(id=position_id))
    #关键的两句输出excel文件
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=export.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'Sheet1')
    #第一行表头  
    sheet.write(0,0, '编号')
    sheet.write(0,1, '名称')
    sheet.write(0,2, '类型')
    sheet.write(0,3, '型号')
    sheet.write(0,4, '单价')
    sheet.write(0,5, '使用人')
    sheet.write(0,6, '位置')
    sheet.write(0,7, '购入时间')
    sheet.write(0,8, '备注')
   
    row = 1
    for item in info:
        sheet.write(row,0, item.id)
        sheet.write(row,1, item.name)
        sheet.write(row,2, item.type.name)
        sheet.write(row,3, item.modelType)
        sheet.write(row,4, item.price)
        sheet.write(row,5, item.user)
        sheet.write(row,6, item.position.name)
        sheet.write(row,7, item.purchasetime)
        sheet.write(row,8, item.remark)
        row=row + 1
       
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response

def _sbgl(request):
    '''设备管理界面'''
    info=None
    clzzs=None
    positions=None
    position=None
    type=None
    position_name='全部'
    type_name='全部'
    type_id=request.GET.get('type_id')
    position_id=request.GET.get('position_id')
    if position_id:
        if int(position_id) != 0:
            position=EquipmentPosition.objects.get(id=position_id)
            position_name=position.name
    else:
        position_id=0
    
    if type_id:
        if int(type_id)!=0:
            type=EquipmentType.objects.get(id=type_id)
            type_name=type.name
    else:
        type_id=0
    try:
        type_id=int(type_id)
        position_id=int(position_id)
        if position_id==0 and type_id==0:
            info=EquipmentBasticInfo.objects.all()
        elif position_id==0 and type_id!=0:
            info=EquipmentBasticInfo.objects.filter(type=type)
        elif type_id==0 and position_id!=0:
            info=EquipmentBasticInfo.objects.filter(position=position)
        else:
            info=EquipmentBasticInfo.objects.filter(type=type,position=position)
        filterstr=request.GET.get('filter')
        if filterstr is not None:
            info=info.filter(remark__contains=filterstr)
        else:
            filterstr=''
        clzzs=EquipmentType.objects.all()
        positions=EquipmentPosition.objects.all()
    except:
        pass
    
    contacts=None
    paginator=Paginator(info,12)
    try:
        contacts=paginator.page(request.GET.get('page',1))
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)
    
    context={'clzzs':clzzs,
             'positions':positions,'type_id':type_id,
             'position_id':position_id,
             'type_name':type_name,
             'position_name':position_name,'res':contacts,
             'filterstr':filterstr}
    
    return context

def _wlzt(request):
    '''网络状态'''
    context={}
    return context

def _bxgl(request):
    '''报修管理'''
    context={}
    return context

def _ptsjtj(request):
    '''报修管理'''
    context={}
    return context

def _grzl(request):
    '''个人资料'''
    context={}
    return context

def _xgmm(request):
    '''修改密码'''
    context={}
    return context
