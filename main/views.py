import json
import pdb
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
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
    card_stuff = []
    for card in Card.objects.all().order_by('name'):
        types = list(card.types.all())
        for excluded_type in EXCLUDED_CARD_TYPES:
            if excluded_type in types:
                break
        else:
            card_stuff.append({'value' : card.name, 'data' : card.id })
    return HttpResponse(json.dumps(card_stuff), "application/json")
    
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
