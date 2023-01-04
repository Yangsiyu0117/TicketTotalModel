# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
from django.utils import timezone

import datetime


# Create your models here.

class FileModel(models.Model):
    title = models.CharField(max_length=200)
    # 文件上传至类似 MEDIA_ROOT/uploads/2019/12/20 的路径下
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = ('文件上传')
        verbose_name_plural = ('文件上传')


class Ticket_Category(models.Model):
    """
    工单大分类
    """

    name = models.CharField(
        verbose_name=u'分类名称',
        max_length=100,
        help_text=('分类名称'),
    )

    title = models.CharField(
        verbose_name=u'分类简介',
        max_length=100,
        help_text=('分类简介概要描述'),
    )

    description = models.TextField(
        verbose_name=u'详情描述信息',
        blank=True,
        null=True,
        help_text=('分类简介概要描述'),
    )

    priority = models.IntegerField(
        verbose_name=u'显示权重级别',
        default=10,
        help_text=('越低显示优先级别越高'),
    )

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('priority',)
        verbose_name = ('工单大分类')
        verbose_name_plural = ('工单大分类')


class Ticket_Subtype(models.Model):
    """
    工单子分类
    """
    category_name = models.CharField(
        verbose_name=u'主分类名称',
        max_length=100,
        help_text=('主分类名称'),
    )

    name = models.CharField(
        verbose_name=u'子分类名称',
        max_length=100,
        help_text=('子分类名称'),
    )

    title = models.CharField(
        verbose_name=u'子分类简介',
        max_length=100,
        help_text=('子分类简介概要描述'),
    )

    description = models.TextField(
        verbose_name=u'子详情描述信息模板',
        blank=True,
        null=True,
        help_text=('子分类模板概要描述'),
    )

    priority = models.IntegerField(
        verbose_name=u'显示权重级别',
        default=100,
        help_text=('越低显示优先级别越高'),
    )

    belong_to = models.ForeignKey(
        Ticket_Category,
        on_delete=models.CASCADE,
        related_name='subtypes',
        blank=True,
        null=True,
        verbose_name=('工单子分类'),
    )

    meta_data = JSONField(null=True, default={}, blank=True, verbose_name=u'Meta  data JSON')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('priority',)
        verbose_name = ('工单子分类')
        verbose_name_plural = ('工单子分类')


class KBItem(models.Model):
    """
    工单知识库

    """
    category_name = models.CharField(
        verbose_name=u'主分类名称',
        max_length=100,
        help_text=('主分类名称'),
    )

    edit_username = models.CharField(
        verbose_name=u'知识编辑人',
        max_length=100,
        help_text=('知识编辑人'),
    )

    category = models.ForeignKey(
        Ticket_Subtype,
        on_delete=models.CASCADE,
        related_name='kbitems',
        verbose_name=('工单子分类'),
    )

    title = models.CharField(
        ('Title'),
        max_length=100,
    )

    answer = models.TextField(
        ('Answer'),
    )

    recommendations = models.IntegerField(
        ('Positive Votes'),
        help_text=('推荐指数'),
        default=0,
    )

    last_updated = models.DateTimeField(
        ('Last Updated'),
        help_text=('最后更新日期'),
        blank=True,
    )

    priority = models.IntegerField(
        ('显示权重级别'),
        default=100,
        help_text=('越低显示优先级别越高'),
    )

    enabled = models.BooleanField(
        ('是否开放对外部显示'),
        default=True,
    )

    def save(self, *args, **kwargs):
        if not self.last_updated:
            self.last_updated = timezone.now()
        return super(KBItem, self).save(*args, **kwargs)

    def __str__(self):
        return '%s: %s' % (self.category.title, self.title)

    class Meta:
        ordering = ('priority', 'title',)
        verbose_name = ('工单知识库')
        verbose_name_plural = ('工单知识库')


class Ticket(models.Model):
    """
     运维工单表

    """

    OPEN_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5

    STATUS_CHOICES = (
        (OPEN_STATUS, ('新工单')),
        (REOPENED_STATUS, ('已分配处理中')),
        (RESOLVED_STATUS, ('已解决工单')),
        (CLOSED_STATUS, ('关闭工单')),
        (DUPLICATE_STATUS, ('重复工单')),
    )

    PRIORITY_CHOICES = (
        (1, ('1. 紧急')),
        (2, ('2. 高')),
        (3, ('3. 普通')),
        (4, ('4. 低')),
        (5, ('5. 待办排期')),
    )

    title = models.CharField(
        ('工单标题'),
        max_length=200,
    )

    ticket_uuid = models.CharField(verbose_name=u'工单ID', default="", max_length=100, help_text="工单ID")
    ticket_category_name = models.CharField(verbose_name=u'工单主分类名称', default="", max_length=100, help_text="主分类名称")
    ticket_type_name = models.CharField(verbose_name=u'工单子分类名称', default="", max_length=100, help_text="子分类名称")

    ticket_type = models.ForeignKey(
        Ticket_Subtype,
        on_delete=models.CASCADE,
        verbose_name=('工单子分类'),
    )

    created_time = models.DateTimeField(
        ('创建时间'),
        auto_now_add=True,
        help_text=('工单创建时间'),
    )

    created_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'提交人')

    created_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="todo_created_by", )

    modified_time = models.DateTimeField(
        ('修改时间'),
        editable=True,
        null=True,
        blank=True,
        help_text=('工单最近更新时间'),
    )

    is_completed = models.BooleanField(default=False, help_text=('工单是否完成'))
    is_del = models.BooleanField(default=False, help_text=('工单是否删除'))
    is_delivery = models.BooleanField(default=False, help_text=('工单答复是否提醒通知'))

    completed_time = models.DateTimeField(
        ('完结时间'),
        editable=True,
        blank=True,
        null=True,
        help_text=('工单关闭时间'),
    )

    sub_users = models.CharField(
        ('Submitter user'),
        max_length=100,
        blank=True,
        null=True,
        help_text=('关注订阅用户'),
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todo_assigned_to",
        blank=True,
        null=True,
        verbose_name=('Assigned to'),
    )

    status = models.IntegerField(
        ('工单状态'),
        choices=STATUS_CHOICES,
        default=OPEN_STATUS,
    )

    on_hold = models.BooleanField(
        ('升级'),
        blank=True,
        default=False,
        help_text=('是否升级工单到高级人员处理'),
    )

    description = models.TextField(
        ('描述信息'),
        blank=True,
        null=True,
        help_text=('工单描述信息'),
    )

    resolution = models.TextField(
        ('解决方案'),
        blank=True,
        null=True,
        help_text=('解决方案结论描述'),
    )

    res_rate_desc = models.TextField(
        ('客户评论意见'),
        blank=True,
        null=True,
        help_text=('客户评论意见'),
    )

    res_rate_value = models.IntegerField(
        ('客户评论分数'),
        default=0,
        blank=True,
        null=True,
        help_text=('客户评论分数'),
    )

    priority = models.IntegerField(
        ('优先级别'),
        choices=PRIORITY_CHOICES,
        default=3,
        blank=3,
        help_text=('1 = Highest Priority, 5 = Low Priority'),
    )

    due_date = models.DateField(
        ('截止日期'),
        blank=True,
        editable=True,
        null=True,
    )

    kbitem = models.ForeignKey(
        "KBItem",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=('关联的知识库FAQ'),
    )

    meta_data = JSONField(null=True, default={}, blank=True, verbose_name=u'Meta  data JSON')

    class Meta:
        ordering = ('-id',)
        verbose_name = ('工单表')
        verbose_name_plural = ('工单表')

    def __str__(self):
        return '%s %s' % (self.id, self.title)
        # return '%s %s %s %s' % (self.id,ticket_category_name, ticket_type_name, self.title)


class Comment(models.Model):
    """
    工单答复记录表
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comment', help_text=('工单来源'))

    answer_time = models.DateTimeField(default=datetime.datetime.now)
    answer_from = models.CharField(max_length=100, blank=True, null=True, help_text=('答复人实名'))
    ticket_from = models.CharField(max_length=100, blank=True, null=True, help_text=('需求人实名'))
    answer_nickname = models.CharField(max_length=100, blank=True, null=True, help_text=('答复人昵称'))
    body = models.TextField(blank=True)
    ticket_owner = models.BooleanField(default=False, help_text=('答复人是否等于问题人'))
    meta_data = JSONField(null=True, default={}, blank=True, verbose_name=u'Meta  data JSON')

    class Meta:
        ordering = ('-id',)
        verbose_name = ('工单答复记录表')
        verbose_name_plural = ('工单答复记录表')

    def __str__(self):
        return '%s %s' % (self.answer_from, self.ticket.title)

    def save(self, **kwargs):
        if self.answer_from == self.ticket.created_name:
            self.ticket_owner = True
            self.answer_nickname = self.answer_from

        super(Comment, self).save()
