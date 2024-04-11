import random
from game import event

class Weather(event.Event):
    '''An event that when triggered determines an occurrence of bad weather.
    Currently instances of bad weather include light rain, heavy rain, and a thunderstorm.
    This event can be further expanded upon in the future to have an effect on the crew and ship, if wanted.'''
    
    def __init__(self):
        self.name = "bad weather"
    
    def process(self, world):
        random_num = random.randint(1,10)
        if random_num < 7:
            msg = "a light rainstorm is occurring"
        elif random_num < 10:
            msg = "a heavy rainstorm is occurring"
        else:
            msg = "a thunderstorm is occurring"

        result = {}
        result["message"] = msg
        result["newevents"] = [ self ]
        return result
