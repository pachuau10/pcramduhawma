from django.urls import path
from . import views

app_name = 'software'

urlpatterns = [
    path('', views.software_list, name='software_list'),
    path('<slug:slug>/', views.software_detail, name='software_detail'),
    path('<slug:slug>/download/', views.software_download, name='software_download'),
]
