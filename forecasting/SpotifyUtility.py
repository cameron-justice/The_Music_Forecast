import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numpy as np

class SpotifyUtility():

    def __init__(self):
        self.client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'))
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


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

            if(index+1 < len(p_values)):
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

