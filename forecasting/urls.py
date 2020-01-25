from django.urls import path

from . import views

urlpatterns = [
    #homepage
    path('', views.forecast, name='forecast'),    
]
