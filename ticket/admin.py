from django.contrib import admin
from ticket.models import *
# Register your models here.
admin.site.register(FileModel)
admin.site.register(Ticket_Category)
admin.site.register(Ticket_Subtype)
admin.site.register(KBItem)
admin.site.register(Ticket)
admin.site.register(Comment)