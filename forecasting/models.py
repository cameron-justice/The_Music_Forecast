from django.db import models

# Create your models here.

class Playlist(models.Model):
    pID = models.TextField()
    title = models.CharField(max_length=50)
    cover = models.ImageField()
    creator = models.CharField(max_length=50)

class WeatherValue(models.Model):
    energy = models.FloatField()
    valence = models.FloatField
    bpm = models.IntegerField()
