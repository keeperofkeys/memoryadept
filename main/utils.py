from django.core.cache import cache
from models import Location, Card
import math

def find_cards(starting_letters):
    starting_letters = starting_letters.lower()
    cards = get_card_list()
    chunk_length = len(starting_letters)
    
    def home_in(jab=len(cards)/2, rang=(0, len(cards)) ):
    # returns index of a card (not necessarily the first) that
    # matches the starting_letters
        card = cards[jab].lower()

        if card.startswith(starting_letters):
            return jab, rang
        
        if starting_letters < card[:chunk_length].lower():
            rang = (rang[0], jab - 1)
            
        else:
            rang = (jab + 1, rang[1])
            
        if rang[1] <= rang[0]: # range has closed up to nothing
            card = cards[rang[0]].lower()
            if card.startswith(starting_letters):
                return rang[0], rang
                
            return None, rang
            
        jab = rang[0] + int(math.ceil((rang[1] - rang[0]) / 2)) 
            
        return home_in(jab, rang)
        
    i, r = home_in()
    if i is None:
        return []
        
    while i > 0 and cards[i-1].lower().startswith(starting_letters):
        i -= 1
    
    ret_list = [cards[i]]
    for j in range(i+1, r[1] +1):
        card = cards[j]
        if card.lower().startswith(starting_letters):
            ret_list.append(card)
        else:
            break
    
    return ret_list
    
def get_excluded_types():
    try:
        return [
            Type.objects.get(name='Plane'),
            Type.objects.get(name='Scheme'),
        ]
    except:
        return []
    
def get_card_tuples():
    card_tuples = cache.get('card_tuples', None)
    if not card_tuples:
        cards = get_card_list()
        card_tuples = [{'value' : re.sub(r'[^a-zA-Z0-9 ]+', '', card), 'data' : card }
            for card in cards]
        cache.set('card_tuples', card_tuples, None)
        
    return card_tuples
    
def get_card_list():
    card_list = cache.get('card_list', [])

    if not card_list:
        for card in Card.objects.all().order_by('name'): 
            types = list(card.types.all())
            for excluded_type in get_excluded_types():
                if excluded_type in types:
                    break
            else:
                card_list.append(card.name)
        
        cache.set('card_list', card_list, None) # cache indefinitely

    return card_list
    
def get_limbo():
    l, __f = Location.objects.get_or_create(name='limbo')
    return l
