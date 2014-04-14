import json
from main.models import *

import pdb

#from django.core.exceptions import DoesNotExist
def go(path="AllSets.json"):
    for (card_data, set_data) in card_generator(path):
        set, new_set_flag = Set.objects.get_or_create(code=set_data['code'],
            name=set_data['name'])
        
        if new_set_flag:
            print set_data['name']

        card_name = card_data['name']
        types = []
        if not 'types' in card_data.keys():
            print 'culprit: %s' % card_data['name']
            continue
            
        for type_name in card_data['types']:
            type, new_type_flag = Type.objects.get_or_create(name=type_name)
            types.append(type)
            
        card, new_card_flag = Card.objects.get_or_create(name=card_name)
        
        card.types = types
        card.sets.add(set)
        card.save()
        
        #printings = list(Card.objects.filter(name=card_name))
        #if card_data['type'].lower() == "scheme":
        #    print card_name
        
        
        #for other_card in printings:
        #    other_card.sets.add(card)
        #    other_card.save()
            

def card_generator(path="AllSets.json"):
    with open(path) as json_file:
        data = json.load(json_file)
        
    for set_id in data.keys():
        set_data = data[set_id]
              
        for card_data in set_data['cards']:            
            yield (card_data, set_data)


