from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class AbandonedIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'A'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}

        self.locations["southBeach"] = self.starting_location
        self.locations["northBeach"] = NorthBeach(self)
        self.locations["westBeach"] = WestBeach(self)
        self.locations["eastBeach"] = EastBeach(self)

        self.locations["hill"] = Hill(self)
        #self.locations["livingStatues"] = LivingStatues(self)
        #self.locations["church"] = Church(self)


    def enter (self, ship):
        print ("You have arrived at an abandoned island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # All beaches have a 25% chancce for a seagull encounter
        self.event_chance = 25
        self.events.append (seagull.Seagull())
        #self.events.append(octopus.Octopus()) # Random Idea I had for an event, an octopus attack

    def enter (self):
        announce ("You arrive at the beach. Your ship is at anchor in a small bay to the south.\n" + 
                  "There is a small hill to the north. It has some sort of ruins on it.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        elif (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
            
class EastBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "eastBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You arrive at the Eastmost side of the island."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]

class WestBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You arrive at the Westmost side of the island"
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]

class NorthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "northBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You arrive at the Northmost side of the island."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]


class Hill (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "hill"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['investigate'] = self
        self.verbs['enter'] = self

    def enter (self):
        edibles = False
        #The description has a base description, followed by variable components.
        description = "You walk to the top of the small hill on the island. There is an abandoned church with three statues next to it.\nYou may investigate the statues and enter the church."

        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
        elif (verb == "enter"):
            #if self.church_open:
            #    config.the_player.next_loc = self.main_location.locations["church"]
            #    config.the_player.go = True
            #else:
            print("You try to open the doors to the church, but they won't budge.")
        
        elif (verb == "investigate"):
            #config.the_player.next_loc = self.main_location.locations["livingStatues"]
            #config.the_player.go = True
            print("The statues loom above you, but nothing happens.")

'''
*****The LivingStatues and Church classes are very rudimentary at the moment, they are very buggy and not fully functional yet.*******
'''

'''
# Class for the Living Statues

class LivingStatues (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = 'livingStatues'
        self.verbs['exit'] = self
        self.verbs['leave'] = self
    
    def enter (self):
        description = "You walk up to the statues, and to your surprise, they start talking to you."
        announce(description)
        self.HandleStatues()

    def process_verb (self, verb, cmd_list, nouns):
        if(verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations[f"hill"]

    def HandleStatues(self):
        print("Statue 2: Hello there travellers!")
        print("Statue 1: Welcome to the island!")
        print("Statue 3: If you wish to enter that old church and seek salvation, you must correctly answer our Knights and Knaves riddle!")

        choice = input("Statue 2: Would you like to answer our riddle? ")
        if ("yes" in choice.lower()):
            self.HandleRiddle()
        else:
            print("-----------------------------------")
            print("Statues: Safe adventures, travellers!")
            print("The statues become dormant once again.")
            print("-----------------------------------")
            config.the_player.next_loc = self.main_location.locations[f"hill"]
            config.the_player.go = True

    # Incomplete
    def HandleRiddle(self):
        riddle = self.GetRiddleAndAnswer()
        guesses = 3

        # While the player still has guesses, ask for their answer and respond appropriately.
        while guesses > 0:
            print(riddle[0])
            plural = ""
            if(guesses != 1):
                plural = "s"
            
            print(f"You may guess {guesses} more time{plural}.") 
            choice = input("What is your guess? ")
            if riddle[1] in choice:
                self.church_open = True
                announce("The doors to the church swing open.")
                return
            else:
                guesses -= 1
                announce("You have guessed incorrectly.")

        if(guesses <= 0):
            print("Statues: Sorry, you ran out of guesses, come back later!")
            config.the_player.next_loc = self.main_location.locations[f"hill"]

# Class for the Church location
class Church (location.Sublocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = 'Old Church'
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['investigate'] = self
        self.shrineUsed = False
    
    def enter (self):
        description = 'Remnants of benches and other debris are scattered about the room.\nThere is a hole in the roof that light shines through, illuminating an altar towards the front of the sanctuary.\nLooming above the altar is a dark statue, seemingly unaffected by time.'
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'exit' or verb == 'leave'):
            config.the_player.next_loc = self.main_location.locations['hill']
            config.the_player.go = True

'''