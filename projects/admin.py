from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'featured', 'published', 'created_at']
    list_filter = ['status', 'featured', 'published', 'created_at']
    search_fields = ['name', 'description', 'technologies']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status', 'featured', 'published']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Details', {
            'fields': ('technologies', 'github_url', 'live_url', 'status')
        }),
        ('Publishing', {
            'fields': ('featured', 'published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
