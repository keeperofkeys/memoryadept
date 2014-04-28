import json
import pdb
import re

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from main.forms import LocationForm
from main.models import Location, Card, Type
from main.utils import get_card_list, get_card_tuples, find_cards

EXCLUDED_CARD_TYPES = [
    Type.objects.get(name='Plane'),
    Type.objects.get(name='Scheme'),
]

@csrf_exempt
def newLocation(request):
    context = {}
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return redirect('location-list')
        else:
            context.update({'form' : form })
    else:
        form = LocationForm()
        context.update({'form' : form })
    return render(request, 'new_location.html', context)
    
def locationList(request):
    context = { 'locations' : Location.objects.all() }
    return render(request, 'choose_location.html', context)
    
def locationEdit(request, location_id=None):

    return render(request, 'edit_location.html', {
            'location_selected' : Location.objects.get(id=location_id) if location_id else None,
            'locations' : Location.objects.all(),
        })

#AJAX stuff
def cardListJSON(request):
    card_tuples = get_card_tuples()
    return HttpResponse(json.dumps(card_tuples), "application/json")
    
def suggestions(request):
    search_string = request.GET.get('query')
    card_list = find_cards(search_string)
    response_list = { 'suggestions' : [{ 'value' : card, 'data' : card } for card in card_list] }
    return HttpResponse(json.dumps(response_list), "application/json")

def location_contents(request, location_id):
    location = Location.objects.get(id=location_id)
    cards = [(card.name, card.cardmap_owner, card.cardmap__is_proxy, card.cardmap__is_foil ) for card in location.cards.all()]
    return HttpResponse(json.dumps(cards), "application/json")
    
def get_or_create_location(request):
    name = request.POST.get('new-location')
    response_obj = {}
    try:
        location, flag = Location.objects.get_or_create(name=name)
        response_obj.update({
            'location_id' : location.id,
            'location_name' : location.name,
            'new' : flag,
        })
        
    except:
        response_obj.update({
            'failed': True,
        })
        
    return HttpResponse(json.dumps(response_obj), "application/json")
    

