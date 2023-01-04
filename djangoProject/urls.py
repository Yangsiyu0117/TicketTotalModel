"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from ticket.views import *
from rest_framework import routers
from django.urls import re_path as url

# 声明一个默认的路由注册器
router = routers.DefaultRouter()
# 注册定义好的接口视图
router.register(r'tickets', TicketViewSet)
router.register(r'files', File_ViewSet)
router.register(r'comments', Comment_ViewSet)
router.register(r'category', Category_ViewSet)
router.register(r'kbi', KBItem_ViewSet)
router.register(r'subtype', Subtype_ViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^API', include(router.urls)),  # restful的根路由
    # path('count/', DayTotalCountView.as_view()),
    url(r'^ticket/', include('ticket.urls')),
    re_path(r'^api-auth', include('rest_framework.urls')),  # 接口认证路由
]
