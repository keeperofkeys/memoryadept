from django.db import models

FORMAT_CHOICES = (
    ('None', ''),
    ('Standard', 's'),
    ('Modern', 'm'),
    ('EDH/Commander', 'e'),
    ('Casual', 'c'),
    ('Legacy', 'l'),
    ('Vintage', 'v'),
)

class Card(models.Model):
    name = models.CharField(max_length=1024)
    
class Person(models.Model):
    name = models.CharField(max_length=100)
    
class CardMap(models.Model):
    location = models.ForeignKey('Location')
    card = models.ForeignKey(Card)
    owner = models.ForeignKey(Person, null=True)
    is_proxy = models.BooleanField(default=False)
    is_foil = models.BooleanField(default=False)
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cards = models.ManyToManyField(Card, through=CardMap)
    owner = models.ForeignKey(Person)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=1)
    
