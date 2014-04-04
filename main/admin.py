from django.contrib import admin
from models import *


class CardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Card, CardAdmin)

class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)

class CardMapInline(admin.TabularInline):
    model = CardMap
    
class LocationAdmin(admin.ModelAdmin):
    inlines = (CardMapInline,)
admin.site.register(Location, LocationAdmin)

