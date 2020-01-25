from django.shortcuts import render
import spotipy
from .models import Playlist

# Create your views here.
def forecast(request):
    weather = getWeather()
    pl = getPlaylist(weather)
    return render(request, 'forecasting/index.html', {'weather': weather, 'playlist': pl})

def getWeather():
    return ""

def getPlaylist(weather):
    return ""
