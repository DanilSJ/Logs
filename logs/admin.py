from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_at',)