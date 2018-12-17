import json
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django import forms
from django.views import generic 
from geopy import distance, Nominatim
from .models import Item, GeoLoc, ItemLocation, ItemResultsRestView


HOME_LOC = settings.DEFAULT_LOC 

class HomeView(generic.TemplateView):
    template_name = 'home.html'


class ItemView(generic.DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        item_obj = self.get_object()
        item_loc = ItemLocation()
        context['locations'] = item_obj.locations.all()

        return context


class ItemListView(generic.ListView):
    model = Item
    template_name = 'item_list.html'


class SearchForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.widgets.CheckboxSelectMultiple)


class SelectItemsView(generic.ListView):
    model = Item
    template_name = 'shop.html'


class ItemCreateView(generic.CreateView):
    model = Item                     # Object we want to create
    template_name = 'item_add.html'  # template that displays the form
    
    # list of attributes we want to display widgets for...
    fields = ['name', 'price', 'image_url']
    success_url = reverse_lazy



# REST API # 
class ItemsResultsRestView(generic.ListView):

    def post(self, request, *args, **kwargs):

        form = SearchForm(request.POST)
        a = (-71.312796, 41.49008)
        b = (-71.312796, 41.49008)
        miles = distance.distance(a, b).miles # 

        total_cost = 0 
        
        name = []
        price = 0
        lat = 0    
        lon = 0

        data = {'items': [], 'miles': miles, 'cost': total_cost}

        if form.is_valid:

            form_data = request.POST.getlist('items')
            item_objects = [] 
            
            for item in form_data:
                item_obj = Item.objects.get(pk=item)
                item_objects.append(item_obj)
        
            #  Begin here to determine optimal item location for each item in item_objects list
            home_location = (HOME_LOC['latitude'], HOME_LOC['longitude'])
            
            for item in item_objects:
                locations = item.locations.all()
                min_location = (locations[0].location.lat, locations[0].location.lon)
                min_miles = distance.distance(min_location, home_location)
                
                for j in locations:
                    location = (j.location.lat, j.location.lon)
                    new_distance = distance.distance(location, home_location).miles
                    
                    if new_distance < min_miles:
                        min_miles = new_distance
                        min_location = j
                
                data['items'].append({
                    'name': min_location.item.name, 
                    'price': min_location.item.price,
                    'lat': min_location.location.lat,
                    'lon': min_location.location.lon})
                data['miles'] = data['miles'] +new_distance
                data['cost'] = data['cost'] + min_location.item.price

            # End local edits here.
        return JsonResponse(data, safe=False)