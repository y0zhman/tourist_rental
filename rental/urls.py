from django.urls import path
from . import views

app_name = 'rental'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
]