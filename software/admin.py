from django.contrib import admin
from .models import Software, SoftwareScreenshot


class SoftwareScreenshotInline(admin.TabularInline):
    model = SoftwareScreenshot
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'platform', 'download_count', 'featured', 'published', 'release_date']
    list_filter = ['published', 'featured', 'platform', 'architecture', 'release_date']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['featured', 'published']
    inlines = [SoftwareScreenshotInline]
    readonly_fields = ['download_count', 'created_at', 'updated_at']
    date_hierarchy = 'release_date'
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'short_description', 'description')
        }),
        ('Version Info', {
            'fields': ('version', 'release_date', 'platform', 'architecture')
        }),
        ('File', {
            'fields': ('file', 'file_size')
        }),
        ('Details', {
            'fields': ('features', 'requirements', 'installation', 'changelog')
        }),
        ('Links', {
            'fields': ('source_url', 'website_url', 'license')
        }),
        ('Publishing', {
            'fields': ('featured', 'published')
        }),
        ('Stats', {
            'fields': ('download_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SoftwareScreenshot)
class SoftwareScreenshotAdmin(admin.ModelAdmin):
    list_display = ['software', 'caption', 'order']
    list_filter = ['software']
