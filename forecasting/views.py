from django.shortcuts import render
from .models import Playlist
from .models import WeatherValue
import requests
import os
import numpy as np
from django.http import HttpResponse
import .SpotifyUtility as SpotUtils

def index(request):
    return render(request, 'forecasting/index.html')

# Create your views here.
def forecast(request):
    sp = SpotUtils.SpotifyUtility()
    weather = getWeather()
    pl = sp.getPlaylist(weather)
    return render(request, 'forecasting/index.html', {'weather': weather, 'playlist': pl})
# Functionality

def updateValues(request):
    PList = Playlist.objects.all()

def getWeather():
    return (0,0,0)

