from django.db import models

FORMAT_CHOICES = (
    ('None', ''),
    ('Standard', 's'),
    ('Modern', 'm'),
    ('EDH/Commander', 'e'),
    ('Casual', 'c'),
    ('Legacy', 'l'),
    ('Vintage', 'v'),
    ('Cube', 'u'),
)

class Set(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    
    def __unicode__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=1024)
    set = models.ForeignKey(Set)
    others = models.ManyToManyField('Card', blank=True, null=True)
    
    def __unicode__(self):
        if len(self.others.all()) > 0:
            return '%s (%s)' % (self.name, self.set)
        else:
            return self.name
    
class Person(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
class CardMap(models.Model):
    location = models.ForeignKey('Location')
    card = models.ForeignKey(Card)
    owner = models.ForeignKey(Person, null=True)
    is_proxy = models.BooleanField(default=False)
    is_foil = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s\'s %s in %s' % (self.owner, self.card, self.location)
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cards = models.ManyToManyField(Card, through=CardMap)
    owner = models.ForeignKey(Person)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=1)
    
    def __unicode__(self):
        return self.name
    
