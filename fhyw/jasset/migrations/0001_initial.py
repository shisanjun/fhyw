# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-04-17 06:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_status', models.PositiveSmallIntegerField(choices=[(1, '上架'), (2, '在线'), (3, '离线'), (4, '下架'), (5, '报废')], default=2, verbose_name='设备状态')),
                ('cabinet_num', models.CharField(max_length=64, verbose_name='机柜编号')),
                ('cabinet_order', models.CharField(help_text='设备在机柜中的位置，从下往上', max_length=64, verbose_name='设备位置')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '资产信息',
                'verbose_name_plural': '资产信息',
                'db_table': 'asset',
            },
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jasset.Asset')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '资产记录表',
                'db_table': 'assetrecord',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='设备类型名称')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '设备类型',
                'verbose_name_plural': '设备类型',
                'db_table': 'devicetype',
            },
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jasset.Asset')),
            ],
            options={
                'verbose_name_plural': '错误日志表',
                'db_table': 'errorlog',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.CharField(max_length=128, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('asset', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='host', to='jasset.Asset', verbose_name='关联资产')),
            ],
            options={
                'verbose_name_plural': '服务器表',
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='HostBasic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('os_platform', models.CharField(blank=True, max_length=16, null=True, verbose_name='系统')),
                ('os_version', models.CharField(blank=True, max_length=16, null=True, verbose_name='系统版本')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basic', to='jasset.Host', verbose_name='所属主机')),
            ],
            options={
                'verbose_name_plural': '基础信息表',
                'db_table': 'hostbasic',
            },
        ),
        migrations.CreateModel(
            name='HostBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(db_index=True, max_length=64, verbose_name='SN号')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='制造商')),
                ('model', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='board', to='jasset.Host', verbose_name='所属主机')),
            ],
            options={
                'verbose_name_plural': '主板表',
                'db_table': 'hostbord',
            },
        ),
        migrations.CreateModel(
            name='HostCPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_count', models.IntegerField(blank=True, null=True, verbose_name='CPU个数')),
                ('cpu_physical_count', models.IntegerField(blank=True, null=True, verbose_name='CPU物理个数')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cpu', to='jasset.Host', verbose_name='所属主机')),
            ],
            options={
                'verbose_name_plural': 'CPU表',
                'db_table': 'hostcpu',
            },
        ),
        migrations.CreateModel(
            name='HostDisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(blank=True, max_length=8, null=True, verbose_name='插槽位')),
                ('model', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘型号')),
                ('size', models.FloatField(blank=True, null=True, verbose_name='磁盘容量GB')),
                ('pd_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘类型')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disk', to='jasset.Host', verbose_name='所属主机')),
            ],
            options={
                'verbose_name_plural': '硬盘表',
                'db_table': 'hostdisk',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='主机组')),
                ('comment', models.TextField(verbose_name='备注')),
            ],
            options={
                'verbose_name': '主机组',
                'verbose_name_plural': '主机组',
                'db_table': 'hostgroup',
            },
        ),
        migrations.CreateModel(
            name='HostMemory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locator', models.CharField(max_length=32, verbose_name='插槽位')),
                ('manufacturer', models.CharField(blank=True, max_length=32, null=True, verbose_name='制造商')),
                ('type', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('size', models.FloatField(blank=True, null=True, verbose_name='容量')),
                ('sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='内存SN号')),
                ('speed', models.CharField(blank=True, max_length=16, null=True, verbose_name='速度')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory', to='jasset.Host', verbose_name='所属主机')),
            ],
            options={
                'verbose_name_plural': '内存表',
                'db_table': 'hostmemory',
            },
        ),
        migrations.CreateModel(
            name='HostNIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='网卡名称')),
                ('hwaddr', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡mac地址')),
                ('netmask', models.CharField(blank=True, max_length=64, null=True)),
                ('ipaddrs', models.CharField(blank=True, max_length=256, null=True, verbose_name='ip地址')),
                ('up', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nic', to='jasset.Host', verbose_name='所属主机')),
            ],
            options={
                'verbose_name_plural': '网卡表',
                'db_table': 'hostnic',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='机房名称')),
                ('floor', models.CharField(max_length=64, verbose_name='楼层')),
            ],
            options={
                'verbose_name': '机房信息',
                'verbose_name_plural': '机房信息',
                'db_table': 'idc',
            },
        ),
        migrations.AlterUniqueTogether(
            name='idc',
            unique_together=set([('name', 'floor')]),
        ),
        migrations.AddField(
            model_name='host',
            name='hostgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jasset.HostGroup', verbose_name='所属主机组'),
        ),
        migrations.AddField(
            model_name='asset',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jasset.DeviceType', verbose_name='设备类型'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jasset.IDC', verbose_name='机房位置'),
        ),
    ]
