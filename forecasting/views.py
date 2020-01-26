from django.shortcuts import render
import spotipy
from .models import Playlist
from .models import WeatherValue
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numpy as np
from django.http import HttpResponse
import ../SpotifyUtility

client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def index(request):
    forecast(request)
    return render(request, 'forecasting/index.html')

# Create your views here.
def forecast(request):
    sp = SpotifyUtility()
    weather = getWeather()
    pl = sp.getPlaylist(weather)
    return render(request, 'forecasting/index.html', {'weather': weather, 'playlist': pl})
# Functionality

def updateValues(request):
    PList = Playlist.objects.all()

def getWeather():
    return (0,0,0)

