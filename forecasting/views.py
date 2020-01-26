from django.shortcuts import render
import spotipy
from .models import Playlist
from .models import WeatherValue
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numpy as np

client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Create your views here.
def forecast(request):
    weather = getWeather()
    pl = getPlaylist(weather)
    return render(request, 'forecasting/index.html', {'weather': weather, 'playlist': pl})

# Functionality

def updateValues(request):
    PList = Playlist.objects.all()

def getWeather():
    return (0,0,0)

def getPlaylist(weather_vals):
    PList = Playlist.objects.all()
    pValues = []
    pIDs = []

    # Append the values and IDs in the same order
    for p in PList:
        pValues.append(calcPlaylistValues(p.pID))
        pIDs.append(p.pID)
    plIndex = getClosestPlaylist(pValues, weather_vals)

    return PList.get(pID=pIDs[plIndex])

def getClosestPlaylist(p_values, w_value):
    closest = None
    nearDist = 100000
    index = 0
    for line in p_values:
        dist = (
            abs(w_value[0] - line[0]),
            abs(w_value[1] - line[1]),
            abs(w_value[2] - line[2])
        )

        for i in range(len(dist)):
            if dist[i] == 0:
                dist[i] += np.random.random(.001, .005)

        sDist = dist[0]*dist[1]*dist[2]
        if sDist < nearDist:
            nearDist = sDist
            closest = index

        index += 1

    return index

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
   
