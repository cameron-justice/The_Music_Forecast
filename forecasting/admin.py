from django.contrib import admin
from .models import Playlist
from .models import WeatherValue

# Register your models here.

admin.site.register(Playlist)
admin.site.register(WeatherValue)
