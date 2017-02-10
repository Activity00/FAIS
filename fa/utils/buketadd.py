#-*-coding:utf-8-*-
#！usr/bin/env python
'''
Created on 2017年2月9日

@author: 武明辉
'''
import datetime
import django
django.setup()
import xlrd
from xlrd.xldate import xldate_as_tuple

from fa.models import EquipmentBasticInfo, EquipmentType, EquipmentPosition




def excel_table_by_name(file_excel='aaa.xlsx',
                        col_name_index=0, by_name='Sheet1'):
    """
        根据名称获取Excel表格中的数据
        参数: file_excel：Excel文件路径
             col_name_index：表头列名所在行的所以
             by_name：Sheet1名称
    """
    data = xlrd.open_workbook(file_excel)
    table = data.sheet_by_name(by_name)
    n_rows = table.nrows   # 行数
    col_names = table.row_values(col_name_index)  # 某一行数据
    row_list =[]
    for row_num in range(1, n_rows):
        row = table.row_values(row_num)
        row_list.append(row)
    return col_names,row_list

def import_unit_batch():
    col_names,data = excel_table_by_name()
    equipment_list = []
    for item in data:
        try:
            type1=EquipmentType.objects.get(name=item[1])
            position=EquipmentPosition.objects.get(name=item[5])
        except:
            continue
        tp=xldate_as_tuple(item[6],0)
        date=datetime.datetime(tp[0],tp[1],tp[2]).strftime('%Y-%m-%d')
        new_info = EquipmentBasticInfo(
                name=item[0],
                type=type1,
                modelType=item[2],
                price=item[3],
                user=item[4],
                position=position,
                purchasetime=date,
                remark=item[7],
            )
        equipment_list.append(new_info)    
    EquipmentBasticInfo.objects.bulk_create(equipment_list)
    print '添加数据成功！'
    
import_unit_batch()

