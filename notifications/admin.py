from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'target', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb')