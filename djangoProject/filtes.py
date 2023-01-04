from django_filters import rest_framework as filters
from ticket.models import *


# from rest_framework import generics

# 创建自定义过滤器类，继承django_filters.rest_framework.FilterSet类
class TicketFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    ticket_category_name = filters.CharFilter(field_name='ticket_category_name', lookup_expr='icontains')
    status = filters.CharFilter(lookup_expr='exact')
    start_date = filters.DateFilter(field_name='created_time', lookup_expr='gte', label='开始时间')  # 大于等于
    end_date = filters.DateFilter(field_name='created_time', lookup_expr='lte', label='结束时间')  # 小于等于

    class Meta:
        # 要对哪个模型数据进行接口过滤
        model = Ticket
        # 过滤的字段，这个字段跟之前的精确查询不一样；是上面自定义的字段，是在接口url后的参数
        fields = ['title', 'ticket_category_name', 'status', 'start_date', 'end_date']
