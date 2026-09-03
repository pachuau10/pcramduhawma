from django.contrib import admin
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'created_at']
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    readonly_fields = ['created_at']
