from django.contrib import admin
from .models import GuestbookEntry


@admin.register(GuestbookEntry)
class GuestbookEntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'message', 'email']
    list_editable = ['is_approved']
    readonly_fields = ['ip_address', 'created_at']
    actions = ['approve_entries', 'disapprove_entries']

    def approve_entries(self, request, queryset):
        queryset.update(is_approved=True)
    approve_entries.short_description = "Approve selected entries"

    def disapprove_entries(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_entries.short_description = "Disapprove selected entries"
