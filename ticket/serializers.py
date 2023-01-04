"""
    当前文件只是为了规定接口的模型及数据字段
"""
from rest_framework import serializers

from ticket.models import *


# Serializers define the API representation.
class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'ticket_category_name', 'status', 'created_time', 'assigned_to_id']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class KBItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = KBItem
        fields = '__all__'


class TicketSubtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Subtype
        fields = '__all__'


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Category
        fields = '__all__'
