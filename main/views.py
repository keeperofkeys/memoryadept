import json
import pdb
import re

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from main.forms import LocationForm
from main.models import Location, Card, Type, CardMap
from main.utils import get_card_list, get_card_tuples, find_cards

try:
    EXCLUDED_CARD_TYPES = [
        Type.objects.get(name='Plane'),
        Type.objects.get(name='Scheme'),
    ]
except:
    EXCLUDED_CARD_TYPES = []

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
    cards = [{ 'count' : cm.quantity, 'name' : cm.card.name }
        for cm in CardMap.objects.filter(location=location)]
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
    
def update_location(request):
    #pdb.set_trace()
    location_id = request.POST.get('location')
    location = Location.objects.get(id=location_id)
    limbo = Location.objects.get(name='limbo')
    new_cards = json.loads(request.POST.get('cards'))
    new_card_names = [name for name in new_cards.keys()]
    new_card_names.sort()
    old_cards = location.cards.all()
    old_card_names = [card.name for card in old_cards]
    old_card_names.sort()
    
    # alphabetic comparison of lists
    ocp = ncp = 0 # pointers
    drop_list = []
    while ocp < len(old_card_names) and ncp < len(new_card_names):
        old_card_name = old_card_names[ocp]
        new_card_name = new_card_names[ncp]
        card = Card.objects.get(name=new_card_name)
        quantity = new_cards[new_card_name]['count']
        if not quantity:
            quantity = 1

        if new_card_name < old_card_name:
            # new_card_name not in existing cards at location
            # TODO: is_foil and other fields on through model
            CardMap.objects.create(card=card, quantity=quantity,
                location=location)
            ncp += 1
            continue
            
        elif new_card_name == old_card_name:
            existing = CardMap.objects.get(card=card, location=location)
            if existing.quantity < quantity:
                existing.quantity = quantity
                existing.save()
                
            elif existing.quantity > quantity:
                removed_count = existing.quantity - quantity
                CardMap.objects.create(location=limbo, card=card, quantity=removed_count)
                drop_list.append({ old_card_name : { 'count' : removed_count } })
                existing.quantity = quantity
                existing.save()

            # else do nothing as same number of that card already there

            ncp += 1
            ocp += 1
            continue
            
        else: # new_card_name > old_card_name => card removed
            old_card = Card.objects.get(name=old_card_name)
            existing = CardMap.objects.get(card=old_card, location=location)
            drop_list.append({ old_card_name : { 'count' : existing.quantity } })
            existing.location = limbo
            existing.save()
            ocp += 1
            continue
        
    #end of while loop
    if ocp >= len(old_card_names): # more new cards left over to add
        for j in range(ncp, len(new_card_names)):
            new_card_name = new_card_names[j]
            card = Card.objects.get(name=new_card_name)
            quantity = new_cards[new_card_name]['count']
            if not quantity:
                quantity = 1
            # TODO: extra through fields
            CardMap.objects.create(location=location, card=card, quantity=quantity)
            
    elif ncp >= len(new_card_names): # more old cards left over to remove
        for j in range(ocp, len(old_card_names)):
            old_card_name = old_card_names[j]
            card = Card.objects.get(name=old_card_name)
            existing = CardMap.objects.get(card=card, location=location)
            drop_list.append({ old_card_name : { 'count' : existing.quantity } })
            existing.location = limbo
            existing.save()

    output = {
        'location_data' : [{ 'count' : cm.quantity, 'name' : cm.card.name }
            for cm in CardMap.objects.filter(location=location)],
        'drop_list' : drop_list,
    }
            
    return HttpResponse(json.dumps(output), "application/json")

