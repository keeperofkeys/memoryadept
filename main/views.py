import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from main.forms import LocationForm
from main.models import Location, Card

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
        #context.update(csrf(request))
        context.update({'form' : form })
    return render(request, 'new_location.html', context)
    
def locationList(request):
    context = { 'locations' : Location.objects.all() }
    return render(request, 'choose_location.html', context)
    
def locationEdit(request, location_id):
    location = Location.objects.get(id=location_id)
    return render(request, 'edit_location.html', {
            'location' : location
        })
    
def cardListJSON(request):
    all_cards = Card.objects.all().order_by('name').distinct()
    return HttpResponse(json.dumps([card.name for card in all_cards]), "application/json") 
