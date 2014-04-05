import json
from main.models import Card

#from django.core.exceptions import DoesNotExist
def go(path="sample_data.json"):
    with open(path) as json_file:
        data = json.load(json_file)
    
    for set_id in data.keys():
        set_data = data[set_id]
        set_name = set_data['name']
        
        for card in set_data['cards']:
            card_name = card['name']
            
            # earlier printing exists
            other_cards = Card.objects.filter(name=card_name)
            db_card = Card.objects.create(
                    name=card_name,
                    set=set_name)
            db_card.others=other_cards
            db_card.save()
            
            for other_card in other_cards:
                other_card.others.add(db_card)
                other_card.save()
            



