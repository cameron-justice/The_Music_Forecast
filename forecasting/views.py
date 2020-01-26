from django.shortcuts import render
import spotipy
from .models import Playlist
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import os

#client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get('CLIENT_KEY'), client_secret=os.environ.get('CLIENT_SECRET'))

# Create your views here.
def forecast(request):
 #   weather = getWeather()
  #  pl = getPlaylist(weather)
    return render(request, 'forecasting/index.html', {'weather': weather, 'playlist': pl})

def updateValues():
    return 0.0

def getWeather():
    return ""

def getPlaylist(weather):
    return ""

def calcPlaylistValues(pID):
    playlist = sp.playlist(pID, fields = None, market = None)
    tracks = playlist['tracks']['items']

    id_list = []

    for i in range(len(tracks)):
        id_list.append(tracks[i]['track']['id'])

    feats = getAudioFeatures(id_list)
    
    eSum = 0.0
    vSum = 0.0
    bSum = 0
    
    count = len(feats['audio_features'])

    for i in range(count):
            eSum += feats['audio_features'][i]['energy']
            vSum += feats['audio_features'][i]['valence']
            bSum += feats['audio_features'][i]['tempo']
    
    return [eSum / count, vSum / count, bSum / count]

def getAudioFeatures(tracks):
    URL = 'https://api.spotify.com/v1/audio-features?ids='

    token = client_credentials_manager._request_access_token()

    auth_header = {'Authorization': 'Bearer ' + token['access_token']}

    PARAMS = {}

    # Make it a csv list
    for track in tracks:
        URL += track + ","

    # remove last comma
    URL = URL[:-1]
    
    r = requests.get(url = URL, params = PARAMS, headers=auth_header)

    return r.json()
   
