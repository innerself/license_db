from django.urls import path

from . import views

app_name = 'license_db'

urlpatterns = [
    path('', views.view, name='view'),
    path('auth/', views.auth, name='auth'),
    path('auth/<str:action>/', views.auth, name='auth'),
    path('import/', views.import_data, name='import_data'),
    path('import/preview/', views.preview_import, name='preview_import'),
    path('import/submit/', views.submit_import, name='submit_import'),
]
