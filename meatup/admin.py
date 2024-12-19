from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')

admin.site.register(Message, MessageAdmin)