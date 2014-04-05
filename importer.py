import json
from main.models import *

import pdb

#from django.core.exceptions import DoesNotExist
def go(path="sample_data.json"):
    with open(path) as json_file:
        data = json.load(json_file)
    
    for set_id in data.keys():
        set_data = data[set_id]
        set, new_set_flag = Set.objects.get_or_create(code=set_data['code'], name=set_data['name'])
        
        for card_data in set_data['cards']:
            card_name = card_data['name']
            
            # earlier printings
            other_cards = list(Card.objects.filter(name=card_name))
            
            #pdb.set_trace()
            
            card, new_card_flag = Card.objects.get_or_create(set=set, name=card_name)
            if len(other_cards):
                card.others=other_cards
                card.save()
            
            for other_card in other_cards:
                other_card.others.add(card)
                other_card.save()
            



