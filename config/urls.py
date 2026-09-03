from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('software/', include('software.urls')),
    path('projects/', include('projects.urls')),
    path('gallery/', include('gallery.urls')),
    path('guestbook/', include('guestbook.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

admin.site.site_header = "PC Ramduhawma's Homepage Admin"
admin.site.site_title = "PC Ramduhawma Admin"
admin.site.index_title = "Website Management"
