from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('data/', views.data),
    path('struktur/', views.struktur),
]