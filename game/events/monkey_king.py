from game import event
import random
from game.combat import Combat
from game.combat import Monster
from game.display import announce
import game.config as config


class MonkeyKing(Monster):
    def __init__(self, name):
        attacks = {}
        attacks["slam"] = ["slams you", random.randrange(75,120), (10,20)]
        attacks["King's Comet"] = ["lays the smackdown on you", random.randrange(110, 125), (10, 20)]
        super().__init__(name, random.randrange(300, 375), attacks, 180 + random.randrange(-5,21))
        self.original = attacks 
        self.new_attack = ["Final Gambit", random.randrange(130, 131), (15, 25)]
        self.low_hp = 100 

    def update_attacks(self):
        if self.health <= self.low_hp:
            print("the King is low on hp and has gained King's Final Gambit")
            self.attacks = {"Final Gambit": self.new_attack}
        else:
            self.attacks = self.original
        
    def getAttacks(self):
        self.update_attacks()
        return super().getAttacks()

class Monkey_King (event.Event):
    '''
    A combat encounter with the monkey king.
    When the event is drawn, creates a combat encounter with 1 monkey king, kicks control over to the combat code to resolve the fight.
    The king is "edible", which is modeled by increasing the ship's food by  20 per kingappearing and adding an apropriate message to the result.
        Since food is good, the event only has a 50% chance to add itself to the result.
    '''

    def __init__ (self):
        self.name = " monkey attack"

    def process (self, world):
        result = {}
        result["message"] = "The Monkey King has been slain!... His spirit has provided a clue for the puzzle on the mountain altar!... The answer is water" 
        monsters = []
        monsters.append(MonkeyKing("Massive Monkey King"))
        announce ("The crew is attacked by the king of the jungle!")
        Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += 7

        return result