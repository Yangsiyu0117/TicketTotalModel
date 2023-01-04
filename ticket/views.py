from django.shortcuts import render
from rest_framework import viewsets
from ticket.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from djangoProject.filtes import TicketFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection


# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
    # 具体返回的数据
    queryset = Ticket.objects.all()
    # 指定过滤的类
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]  # 采用哪个过滤器
    filterset_class = TicketFilter  # 进行查询的字段


class File_ViewSet(viewsets.ModelViewSet):
    # 具体返回的数据
    queryset = FileModel.objects.all()
    # 指定过滤的类
    serializer_class = FileSerializer


class Comment_ViewSet(viewsets.ModelViewSet):
    # 具体返回的数据
    queryset = Comment.objects.all()
    # 指定过滤的类
    serializer_class = CommentSerializer


class Category_ViewSet(viewsets.ModelViewSet):
    # 具体返回的数据
    queryset = Ticket_Category.objects.all()
    # 指定过滤的类
    serializer_class = TicketCategorySerializer


class KBItem_ViewSet(viewsets.ModelViewSet):
    # 具体返回的数据
    queryset = KBItem.objects.all()
    # 指定过滤的类
    serializer_class = KBItemSerializer


class Subtype_ViewSet(viewsets.ModelViewSet):
    # 具体返回的数据
    queryset = Ticket_Subtype.objects.all()
    # 指定过滤的类
    serializer_class = TicketSubtypeSerializer


# 当日新增，解决、处理中的ticket数量
class DayTotalCountView(APIView):
    queryset = Ticket.objects.all()

    def get(self, request):
        today = datetime.datetime.today()
        one_day = today.day
        open_count = Ticket.objects.filter(created_time__day=one_day, status=1).count()
        reopen_count = Ticket.objects.filter(created_time__day=one_day, status=2).count()
        resolved_count = Ticket.objects.filter(created_time__day=one_day, status=3).count()
        return Response({
            'new_ticket_count': open_count,
            'reopen_ticket_count': reopen_count,
            'resolved_ticket_count': resolved_count,
            'date': today
        })


class UserTotalCountView(APIView):
    queryset = Ticket.objects.all()

    def get(self, request):
        today = datetime.datetime.today()
        yangsiyu_resoveld_ticket = Ticket.objects.filter(assigned_to_id=1, status=3).count()
        wentian_resoveld_ticket = Ticket.objects.filter(assigned_to_id=2, status=3).count()
        zhangxiang_resoveld_ticket = Ticket.objects.filter(assigned_to_id=3, status=3).count()

        return Response({
            'name': "yangsiyu",
            'count1': yangsiyu_resoveld_ticket,
            'name2': "wentian",
            'count2': wentian_resoveld_ticket,
            'name3': "zhangxiang",
            'count3': zhangxiang_resoveld_ticket,
            'date': today

        })


class MonthTotalCount(APIView):
    queryset = Ticket.objects.all()

    def get(self, request):
        data = request.GET.get('month_id')
        # today = datetime.datetime.today()
        month_open_count = Ticket.objects.filter(created_time__month=data, status=1).count()
        month_resolved_count = Ticket.objects.filter(created_time__month=data, status=3).count()

        return Response({
            'month_open_count': month_open_count,
            'month_resolved_count': month_resolved_count,
            'date': "查询月份:" + data
        })


class SubtypeTotalCount(APIView):
    queryset = Ticket.objects.all()

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute(
            "select ticket_ticket_subtype.name,COUNT(*) AS subtypeSum from ticket_ticket_subtype inner join ticket_ticket ON  ticket_ticket_subtype.id = ticket_ticket.ticket_type_id group by ticket_ticket.ticket_type_id, ticket_ticket_subtype.name")

        rows = cursor.fetchall()
        rows = dict(rows)

        return Response({
            'sub_count': rows
        })
