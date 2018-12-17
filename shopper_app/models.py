from django.db import models
from django.conf import settings
from geopy import distance
from geopy import geocoders
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import geopy



# (e.g., HOME_LOC['latitude'] or HOME_LOC['longitude'])
HOME_LOC = settings.DEFAULT_LOC

class GeoLoc(models.Model):
    postal_code = models.IntegerField(unique=True)
    city = models.CharField(max_length=128)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.city


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()
    image_url = models.URLField(null=True, blank=True)
    #item_locs = models.CharField(null=True, max_length=128)
    #distance_to_origin = models.CharField(null=True, max_length=128)

    def __str__(self):
        return self.name  # returns a string rep of the object


class ItemResultsRestView(models.Model):
    """Associates an item with a location. An item can be found in multiple locations.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='locitem')
    location = models.ForeignKey(GeoLoc, on_delete=models.CASCADE, related_name='itemloc')
    #name = models.CharField(max_length=128)
    price = models.IntegerField()
    
#    def distance_calculator(location):
#        geolocator = Nominatim(user_agent="shopper_app")
#        lat = geolocator.geocode(location)
#        lon = geolocator.geocode(location)
#        itemloc = str(lat.latitude), str(lon.longitude)
#        home_lat = HOME_LOC['latitude']
#       home_lon = HOME_LOC['longitude']
#        home_loc = home_lat, home_lon
#        dist = geodesic(home_loc, itemloc).miles
        #def distance_to_origin(self):
#        def __str__(self):
#            return self.dist
    


    class Meta:
        unique_together = (('location', 'item'),)

    def __str__(self):
        return self.item.name + '-' + self.location.city









class ItemLocation(models.Model):
    """Associates an item with a location. An item can be found in multiple locations.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='locations')
    location = models.ForeignKey(GeoLoc, on_delete=models.CASCADE, related_name='items')
    
#    def distance_calculator(location):
#        geolocator = Nominatim(user_agent="shopper_app")
#        lat = geolocator.geocode(location)
#        lon = geolocator.geocode(location)
#        itemloc = str(lat.latitude), str(lon.longitude)
#        home_lat = HOME_LOC['latitude']
#       home_lon = HOME_LOC['longitude']
#        home_loc = home_lat, home_lon
#        dist = geodesic(home_loc, itemloc).miles
        #def distance_to_origin(self):
#        def __str__(self):
#            return self.dist
    


    class Meta:
        unique_together = (('location', 'item'),)

    def __str__(self):
        return self.item.name + '-' + self.location.city






