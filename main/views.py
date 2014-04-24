import json
import pdb
import re

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from main.forms import LocationForm
from main.models import Location, Card, Type

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
    card_stuff = _get_card_tuples()
    return HttpResponse(json.dumps(card_stuff), "application/json")
    
def suggestions(request):
    search_string = request.GET.get('query')
    card_list
    
def location_contents(request, location_id):
    location = Location.objects.get(id=location_id)
    #pdb.set_trace()
    cards = [(card.name, card.cardmap_owner, card.cardmap__is_proxy, card.cardmap__is_foil ) for card in location.cards.all()]
    return HttpResponse(json.dumps(cards), "application/json")
    
def get_or_create_location(request):
    name = request.POST.get('new-location')
    response_obj = {}
    try:
        #pdb.set_trace()
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
    
def _find_cards(starting_letters):
    cards = _get_card_list()
    bisector = len(cards) / 2
    card = cards[bisector]
    if card.startswith(starting_letters):
        ret_list = [card]
        bisector += 1
        while cards[bisector].startswith(starting_letters):
            ret_list.append(cards[bisector])
            bisector += 1
    
def _get_card_tuples():
    card_tuples = None# cache.get('card_tuples', None)
    if not card_tuples:
        cards = _get_card_list()
        card_tuples = [{'value' : re.sub(r'[^a-zA-Z0-9 ]+', '', card), 'data' : card }
            for card in cards]
        cache.set('card_tuples', card_tuples, None)
        
    return card_tuples
    
def _get_card_list():
    card_list = []# cache.get('card_list', [])

    if not card_list:
        for card in Card.objects.all().order_by('name'):
            types = list(card.types.all())
            for excluded_type in EXCLUDED_CARD_TYPES:
                if excluded_type in types:
                    break
            else:
                card_list.append(card.name)
        
        cache.set('card_list', card_list, None) # cache indefinitely

    return card_list
