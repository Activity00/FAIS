#-*-coding:utf-8-*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class EquipmentBasticInfo(models.Model):
    name=models.CharField('设备名称',max_length=20)
    type=models.ForeignKey('EquipmentType',on_delete=models.CASCADE,verbose_name='设备类型')
    modelType=models.CharField('设备型号',max_length=20)
    price=models.IntegerField('设备单价')
    user=models.CharField('使用人',max_length=10)
    position=models.ForeignKey('EquipmentPosition',on_delete=models.CASCADE,verbose_name='所在位置')
    purchasetime=models.DateField('购买时间')
    remark=models.CharField('备注',max_length=50,default='')
    
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '设备基本信息'
        verbose_name_plural='设备基本信息表'

class EquipmentType(models.Model):
    name=models.CharField('类型名称',max_length=20,unique=True)
    
    def __str__(self):
        self.name
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '设备类型'
        verbose_name_plural='设备类型表'
        
class EquipmentPosition(models.Model):
    name=models.CharField('位置',max_length=20,unique=True)
    
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '位置'
        verbose_name_plural='位置表'      
    