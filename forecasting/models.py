from django.db import models

# Create your models here.

class Playlist(models.Model):
    pID = models.TextField()
    title = models.CharField(max_length=50)
    cover = models.ImageField()
