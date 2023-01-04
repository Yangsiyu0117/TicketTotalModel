# Generated by Django 4.1.4 on 2022-12-20 02:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
            ],
            options={
                'verbose_name': '文件上传',
                'verbose_name_plural': '文件上传',
            },
        ),
        migrations.CreateModel(
            name='KBItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(help_text='主分类名称', max_length=100, verbose_name='主分类名称')),
                ('edit_username', models.CharField(help_text='知识编辑人', max_length=100, verbose_name='知识编辑人')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('answer', models.TextField(verbose_name='Answer')),
                ('recommendations', models.IntegerField(default=0, help_text='推荐指数', verbose_name='Positive Votes')),
                ('last_updated', models.DateTimeField(blank=True, help_text='最后更新日期', verbose_name='Last Updated')),
                ('priority', models.IntegerField(default=100, help_text='越低显示优先级别越高', verbose_name='显示权重级别')),
                ('enabled', models.BooleanField(default=True, verbose_name='是否开放对外部显示')),
            ],
            options={
                'verbose_name': '工单知识库',
                'verbose_name_plural': '工单知识库',
                'ordering': ('priority', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Ticket_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='分类名称', max_length=100, verbose_name='分类名称')),
                ('title', models.CharField(help_text='分类简介概要描述', max_length=100, verbose_name='分类简介')),
                ('description', models.TextField(blank=True, help_text='分类简介概要描述', null=True, verbose_name='详情描述信息')),
                ('priority', models.IntegerField(default=10, help_text='越低显示优先级别越高', verbose_name='显示权重级别')),
            ],
            options={
                'verbose_name': '工单大分类',
                'verbose_name_plural': '工单大分类',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Ticket_Subtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(help_text='主分类名称', max_length=100, verbose_name='主分类名称')),
                ('name', models.CharField(help_text='子分类名称', max_length=100, verbose_name='子分类名称')),
                ('title', models.CharField(help_text='子分类简介概要描述', max_length=100, verbose_name='子分类简介')),
                ('description', models.TextField(blank=True, help_text='子分类模板概要描述', null=True, verbose_name='子详情描述信息模板')),
                ('priority', models.IntegerField(default=100, help_text='越低显示优先级别越高', verbose_name='显示权重级别')),
                ('meta_data', jsonfield.fields.JSONField(blank=True, default={}, null=True, verbose_name='Meta  data JSON')),
                ('belong_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subtypes', to='ticket.ticket_category', verbose_name='工单子分类')),
            ],
            options={
                'verbose_name': '工单子分类',
                'verbose_name_plural': '工单子分类',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='工单标题')),
                ('ticket_uuid', models.CharField(default='', help_text='工单ID', max_length=100, verbose_name='工单ID')),
                ('ticket_category_name', models.CharField(default='', help_text='主分类名称', max_length=100, verbose_name='工单主分类名称')),
                ('ticket_type_name', models.CharField(default='', help_text='子分类名称', max_length=100, verbose_name='工单子分类名称')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='工单创建时间', verbose_name='创建时间')),
                ('created_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='提交人')),
                ('modified_time', models.DateTimeField(blank=True, help_text='工单最近更新时间', null=True, verbose_name='修改时间')),
                ('is_completed', models.BooleanField(default=False, help_text='工单是否完成')),
                ('is_del', models.BooleanField(default=False, help_text='工单是否删除')),
                ('is_delivery', models.BooleanField(default=False, help_text='工单答复是否提醒通知')),
                ('completed_time', models.DateTimeField(blank=True, help_text='工单关闭时间', null=True, verbose_name='完结时间')),
                ('sub_users', models.CharField(blank=True, help_text='关注订阅用户', max_length=100, null=True, verbose_name='Submitter user')),
                ('status', models.IntegerField(choices=[(1, '新工单'), (2, '已分配处理中'), (3, '已解决工单'), (4, '关闭工单'), (5, '重复工单')], default=1, verbose_name='工单状态')),
                ('on_hold', models.BooleanField(blank=True, default=False, help_text='是否升级工单到高级人员处理', verbose_name='升级')),
                ('description', models.TextField(blank=True, help_text='工单描述信息', null=True, verbose_name='描述信息')),
                ('resolution', models.TextField(blank=True, help_text='解决方案结论描述', null=True, verbose_name='解决方案')),
                ('res_rate_desc', models.TextField(blank=True, help_text='客户评论意见', null=True, verbose_name='客户评论意见')),
                ('res_rate_value', models.IntegerField(blank=True, default=0, help_text='客户评论分数', null=True, verbose_name='客户评论分数')),
                ('priority', models.IntegerField(blank=3, choices=[(1, '1. 紧急'), (2, '2. 高'), (3, '3. 普通'), (4, '4. 低'), (5, '5. 待办排期')], default=3, help_text='1 = Highest Priority, 5 = Low Priority', verbose_name='优先级别')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='截止日期')),
                ('meta_data', jsonfield.fields.JSONField(blank=True, default={}, null=True, verbose_name='Meta  data JSON')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_assigned_to', to=settings.AUTH_USER_MODEL, verbose_name='Assigned to')),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_created_by', to=settings.AUTH_USER_MODEL)),
                ('kbitem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.kbitem', verbose_name='关联的知识库FAQ')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket_subtype', verbose_name='工单子分类')),
            ],
            options={
                'verbose_name': '工单表',
                'verbose_name_plural': '工单表',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='kbitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kbitems', to='ticket.ticket_subtype', verbose_name='工单子分类'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_time', models.DateTimeField(default=datetime.datetime.now)),
                ('answer_from', models.CharField(blank=True, help_text='答复人实名', max_length=100, null=True)),
                ('ticket_from', models.CharField(blank=True, help_text='需求人实名', max_length=100, null=True)),
                ('answer_nickname', models.CharField(blank=True, help_text='答复人昵称', max_length=100, null=True)),
                ('body', models.TextField(blank=True)),
                ('ticket_owner', models.BooleanField(default=False, help_text='答复人是否等于问题人')),
                ('meta_data', jsonfield.fields.JSONField(blank=True, default={}, null=True, verbose_name='Meta  data JSON')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(help_text='工单来源', on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='ticket.ticket')),
            ],
            options={
                'verbose_name': '工单答复记录表',
                'verbose_name_plural': '工单答复记录表',
                'ordering': ('-id',),
            },
        ),
    ]