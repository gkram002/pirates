#Kevin Li's Event

from game import event
import random
import game.config as config

class Doldrum(event.Event):
    '''The event is that there is no wind so the ship is motionless for a couple of days'''
    def __init__(self):
        self.name = ' a lack of wind'

    def process(self, world):
        c = config.the_player.get_world()
        days = c.get_ship()
        days_passed = random.randint(1,3)
        msg = f'Due to having no winds, the ship was stuck for {days_passed} days'
        for i in range(0, days_passed):
            days.end_day(c)
            days.start_day(c)
        c.day += days_passed

        result = {}
        result['message'] = msg
        result['newevents'] = [self]
        return result
        


