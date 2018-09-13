from django.urls import path

from . import views

app_name = 'license_db'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('auth/<str:action>/', views.auth, name='auth'),
]
