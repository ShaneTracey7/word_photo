from django.urls import path, re_path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('data/', views.handleImage, name='data'),
]