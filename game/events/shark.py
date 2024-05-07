from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Shark (Context, event.Event):
    '''Encounter with a crazed  shark. Uses the parser to decide what to do about it.'''
    def __init__ (self):
        super().__init__()
        self.name = "sharky"
        self.sharks = 1
        self.verbs["scare"] = self
        self.verbs["feed "] = self
        self.verbs['help'] = self
        self.verbs['play'] = self
        self.verbs['ride'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "scare"):
            self.go = True
            r = random.randint(1, 5)
            if (r == 5):
                self.result["message"] = ("the giant shark was scared away by your immense strength")
                if (self.sharks >= 1):
                    self.sharks = self.sharks - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "Luckily the giant shark was scared away from your group."
                else:
                    self.result["message"] = c.get_name() + " is attacked by the giant shark ."
                    if (c.inflict_damage (self.sharks, "eaten by shark")):
                        self.result["message"] = ".. " + c.get_name() + " was tragically eaten by a shark!"
        elif (verb == "ride"):
             self.go = True
             r = random.randint(1, 10)
             if (r >= 8):
                 print("The shark has declared you a worthy opponent and you are now its master")
             else:
                 print("the shark is now getting angry")
        elif (verb == "feed"):
            self.sharks = self.sharks + 1
            self.result["newevents"].append(Shark())
            self.result["message"] = "the shark is now happy"
            self.go = True
        elif (verb == "play"):
            print ("You played with the shark and it seems to like you")
            print ("looks like you've made a new friend")
            if (self.sharks > 1):
                    self.sharks = self.sharks - 1
            self.go = False
        elif (verb == "help"):
            print ("apparently you can't help the shark")
            self.go = False
        else:
            print ("why would you want to help the shark?")
            self.go = False




    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.sharks) + " Oh! a wild shark has appeared!")
            Player.get_interaction ([self])

        return self.result
