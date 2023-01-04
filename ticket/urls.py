from django.urls import re_path as url
from ticket.views import *

from django.urls import path, re_path


urlpatterns = [
    url(r'day_count/$', DayTotalCountView.as_view()),
    url(r'user_count/$', UserTotalCountView.as_view()),
    url(r'month_ticket/$', MonthTotalCount.as_view()),
    url(r'sub_ticket/$', SubtypeTotalCount.as_view()),
]