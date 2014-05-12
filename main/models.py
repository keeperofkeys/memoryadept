import re

from django.db import models

FORMAT_CHOICES = (
    ('', 'None'),
    ('s', 'Standard'),
    ('m', 'Modern'),
    ('e', 'EDH/Commander'),
    ('c', 'Casual'),
    ('l', 'Legacy'),
    ('v', 'Vintage'),
    ('u', 'Cube'),
)

class Set(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    
    def __unicode__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=1024)
    search_name = models.CharField(max_length=1024, blank=True, editable=False)
    types = models.ManyToManyField(Type, blank=True)
    sets = models.ManyToManyField(Set, blank=True, null=True)
    search_name = models.CharField(max_length=1024)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        if not self.search_name:
            self.search_name = re.sub(r'[^a-zA-Z0-9 ]+', '', self.name) # TODO: handle accents etc
        super(Card, self).save(*args, **kwargs)
    
class Person(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
class CardMap(models.Model):
    location = models.ForeignKey('Location')
    card = models.ForeignKey(Card)
    owner = models.ForeignKey(Person, null=True, blank=True)
    is_proxy = models.BooleanField(default=False)
    is_foil = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    
    def __unicode__(self):
        return '%s\'s %s in %s' % (self.owner, self.card, self.location)
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cards = models.ManyToManyField(Card, through=CardMap, blank=True)
    owner = models.ForeignKey(Person, blank=True, null=True)
    format = models.CharField(choices=FORMAT_CHOICES, blank=True, max_length=1, default='')
    is_in = models.ForeignKey('Location', null=True, blank=True, default=None)
    
    def __unicode__(self):
        return self.name
    
