from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from main.forms import LocationForm
from main.models import Location

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
