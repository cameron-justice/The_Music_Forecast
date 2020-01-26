from django.urls import path

from . import views

urlpatterns = [
    #homepage
    path('', views.index, name='index'),    
    path('forecast', views.forecast, name='forecast'),
]
