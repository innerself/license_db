from django.urls import path

from . import views

app_name = 'license_db'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('auth_out/', views.auth_out, name='auth_out'),
]
