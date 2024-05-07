from game import event
import random
from game.combat import Combat
from game.combat import Monster
from game.display import announce
import game.config as config

class Goat(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["ram"] = ["rams you",random.randrange(60,100), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))


class Angry_Goats (event.Event):
    '''
    A combat encounter with a troop of agitated goats.
    When the event is drawn, creates a combat encounter with 2 to 4 goats, kicks control over to the combat code to resolve the fight.
    The monkies are "edible", which is modeled by increasing the ship's food by 6 per goat appearing and adding an apropriate message to the result.
        Since food is good, the event only has a 50% chance to add itself to the result.
    '''

    def __init__ (self):
        self.name = " goat attack"

    def process (self, world):
        result = {}
        result["message"] = "the goats are defeated! ...Those look pretty tasty!"
        monsters = []
        n_appearing = random.randrange(2,4)
        n = 1
        while n <= n_appearing:
            monsters.append(Goat("3-eyed Angry Goat "+str(n)))
            n += 1
        announce ("The crew is attacked by a tribe of angry goats!")
        Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*3

        return result