from django.forms import ModelForm
import main.models as m

class LocationForm(ModelForm):
    class Meta:
        model = m.Location
        fields = ['name', 'description', 'cards', 'owner', 'format']
