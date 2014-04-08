from django.shortcuts import render
from main.forms import LocationForm

def newLocation(request):
    form = LocationForm()
    
    return render(request, 'new_location.html', {'form' : form })
