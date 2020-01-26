#!/usr/bin/python

from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
from darksky.forecast import Forecast 
from geopy.geocoders import Nominatim
from datetime import datetime

class WeatherUtility:
    API_KEY = '9eb2c367bb175398754ac86f4f47a6b9'
    darksky = DarkSky(API_KEY)
    geolocator = Nominatim(user_agent = "The Music Forecast")
    
    def __init__(self):
        self.weatherData = {}

    def getWeather(self,location):
        geocode = self.getGeocode(location)

        forecast = self.getWeatherInfo(geocode)

        time = forecast.currently.time
        intensity = forecast.currently.precip_intensity
        precip_type = forecast.currently.precip_type
        temp = forecast.currently.temperature
        wind_speed = forecast.currently.wind_speed
        cloud_cover = forecast.currently.cloud_cover
        visibility = forecast.currently.visibility

        self.weatherData = {forecast.currently.temperature, forecast.currently.summary}
        print(self.weatherData)
        BPM = self.getBPM(temp, wind_speed, intensity, time)
        valence = self.getValence(cloud_cover, visibility, time, intensity, temp)
        energy = self.getEnergy(intensity, time, wind_speed, visibility, cloud_cover)
    
        weights = tuple([round(BPM, 2), round(valence, 2), round(energy, 2)])
        print(weights)
        return weights #tuple

    def getGeocode(self,location):    
        geocode = self.geolocator.geocode(location)
        print(geocode.address)
        if geocode.address[-24:] == 'United States of America':
            geocode = self.geolocator.geocode("Murfreesboro, TN")
        
        return geocode

    def getWeatherInfo(self,geocode):
        latitude = geocode.latitude
        longitude = geocode.longitude

        forecast = self.darksky.get_forecast(
            latitude, longitude,
            extend=False, # default `False`
            lang=languages.ENGLISH, # default `ENGLISH`
            units=units.AUTO, # default `auto`
            exclude=[weather.MINUTELY, weather.ALERTS], # default `[]`,
        )

        return forecast

    def getBPM(self, temp, wind_speed, precip_intensity, time):
        temp_wght = 0.15
        wind_spd_wght = 0.35
        intensity_wght = 0.4 
        time_wght = 0.1

        temperature = self.getTemp(temp)
        wind = self.getWind(wind_speed)
        intensity = self.getIntensity(precip_intensity)
        time_decimal = self.getTime(time)

        BPM = (temp_wght * temperature + wind_spd_wght * wind + intensity_wght * intensity + time_wght * time_decimal)
        BPM += 0.625

        return BPM * 80

    def getValence(self,cloud_cover, visibility, time, precip_intensity, temp):
        cloud_wght = 0.35
        vis_wght = 0.1 
        time_wght = 0.1
        intensity_wght = 0.3 
        temp_wght = 0.15

        vis = self.getVisibility(visibility)
        time_decimal = self.getTime(time)
        intensity = self.getIntensity(precip_intensity)
        temperature = self.getTemp(temp)

        valence = cloud_wght * cloud_cover + vis_wght * vis + time_wght * (1-time_decimal) + intensity_wght * intensity + temp_wght * temperature

        return 1-valence

    def getEnergy(self,precip_intensity, time, wind_speed, visibility, cloud_cover):
        intensity_wght = 0.35
        time_wght = 0.1
        wind_spd_wght = 0.35
        vis_wght = 0.05 
        cloud_wght = 0.15

        intensity = self.getIntensity(precip_intensity)
        time_decimal = self.getTime(time)
        wind = self.getWind(wind_speed)
        vis = self.getVisibility(visibility)

        energy = intensity_wght * intensity + time_wght * time_decimal + wind_spd_wght * wind + vis_wght * vis + cloud_wght * (1-cloud_cover)
        
        return energy

    def getWind(self,wind_speed):
        wind_val = (wind_speed / 75) 
        
        #print ('wind_val',wind_val)
        return wind_val

    def getTemp(self,temp):
        temp_val = 0
        if temp > 60:
            temp_val = 1 - ((float(temp) - 60) / 50)
        else:
            temp_val = 1 - ((60 - float(temp)) / 80) 
            
        
        #print('temp_val',temp_val)
        return temp_val
        
    def getVisibility(self,visibility):
        vis_mod = 0
        if visibility >= 3.1:
            vis_mod = (( visibility * -0.25 ) / 6.9 ) + ( 0.25 / 6.9 )
        elif visibility >= 1.2:
            vis_mod = (( visibility * -0.25 ) / 1.9 ) + ( 1.25 / 1.9 )
        elif visibility >= 0.62:
            vis_mod = (( visibility * -0.25 ) / 0.58 ) + ( .59 / 0.58 )
        else:
            vis_mod = (( visibility * -0.25 ) / 0.62 ) + 1

        #print('visbility',vis_mod)
        return vis_mod

    def getIntensity(self,precip_intensity):
        intensity = 0

        if precip_intensity > 0:
            intensity = precip_intensity / 1.2
                
        #print('intensity',intensity)
        return intensity

    def getTime(self,time):
        hour = int(time.hour)
        value = 0
        if 6 < hour <= 18:
            value = 0.75
        else:
            value = 0.25
        return value
            

    def test(self):
        temp = float (input('Temp: '))
        wind_speed = float (input('Wind Speed: '))
        intensity = float (input('Intensity: '))
        #time = input('Time:')
        cloud_cover = float (input('Cloud Cover: '))
        visibility = float (input('Visibility:'))
        time  = datetime.now()
        
        print('bpm ', self.getBPM(temp, wind_speed, intensity, time))
        print('valence ',self.getValence(cloud_cover, visibility, time, intensity, temp))
        print('energy ',self.getEnergy(intensity, time, wind_speed, visibility, cloud_cover))

b = WeatherUtility()

b.getWeather("Murfreesboro")

