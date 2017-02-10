# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 05:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fa', '0002_auto_20170209_0812'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u8bbe\u5907\u540d\u79f0')),
            ],
        ),
        migrations.AlterField(
            model_name='equipmentbasticinfo',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fa.EquipmentType', verbose_name='\u8bbe\u5907\u7c7b\u578b'),
        ),
    ]