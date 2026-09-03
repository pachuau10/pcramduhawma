from django.contrib import admin
from .models import SiteSettings, VisitorLog, VisitorCount, Link, NavigationItem, ContactMessage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'tagline', 'email']
    readonly_fields = ['created_date']

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'path', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ip_address', 'path']
    readonly_fields = ['ip_address', 'user_agent', 'path', 'referer', 'session_key', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False


@admin.register(VisitorCount)
class VisitorCountAdmin(admin.ModelAdmin):
    list_display = ['total_visits', 'unique_visitors', 'last_updated']
    readonly_fields = ['total_visits', 'unique_visitors', 'last_updated']

    def has_add_permission(self, request):
        if VisitorCount.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip_address', 'created_at']
