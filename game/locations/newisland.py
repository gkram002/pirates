from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

class NewIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'W'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["jungle"] = Jungle(self)
        self.locations["mountain"] = Mountain(self)
        self.locations["riddle"] = Riddle(self)
        self.locations["king"] = King(self)

    def enter (self, ship):
        print ("you have arrived at a mysterious island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        #make a new mob
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ("arrive at the beach. Your ship is at anchor in a moon shaped cove on the south end.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You choose to return to the ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["jungle"]
        elif (verb == "east"):
            announce ("You walk all the way around the island on the beach. It's not very interesting.")
        elif(verb == "west"):
            config.the_player.next_loc = self.main_location.locations["mountain"]

#JUNGLE
class Jungle (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "jungle"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = Claymore()
        self.item_in_clothes = items.Flintlock()

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into a lush jungle on the island."
        if edibles == False:
             description = description + " Nothing around here looks like it could be edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tall tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of ragged fabric on the moist ground."
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["beach"]
            print("You fear too much of the jungle and have ventured back to the safe beach")
        elif (verb == "north"):
            print("a clue to a riddle has appeared the answer you seek is something you burn")
        elif(verb == "east"):
            print("an answer to an easier riddle what are islands surrounded by? ")
        elif(verb == "west"):
             print("you see a path and hear a loud grumbling that you decide to check out")
             config.the_player.next_loc = self.main_location.locations["king"]
             

        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")


class Mountain(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "mountain"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_on_mountain = Claymore()
        self.item_in_clothes = items.Flintlock()

        self.event_chance = 50
        self.events.append(angry_goats.Angry_Goats())
        self.events.append(seagull.Seagull())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, angry_goats.Angry_Goats):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You hiked up to the top of the mountain."
        if edibles == False:
             description = description + " The land looks scarce of any food like substances but it looks as if you can walk around."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_on_mountain != None:
            description = description + " You see a " + self.item_on_mountain.name + " stuck in a tall tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of ragged fabric on the moist ground."
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["beach"]
            print("you decide to make a long trek down the mountain")
        elif (verb == "north"):
            print("you arrive at an altar do you wish to touch it?")
            answer = input("Enter yes or no: ")
            if answer.lower() == "yes":
                self.main_location.locations["riddle"]
                config.the_player.next_loc = self.main_location.locations["riddle"]
            elif answer.lower() == "no":
                print("You decide not touch it out of fear")
            else: 
                print("The heavens command you to enter yes or no. ")

        elif(verb == "west" or verb == "east"):
            print("nothing of importance just a beautiful view")

        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_on_mountain == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_on_mountain
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_on_mountain = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")
class Riddle(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "riddle"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.incorrect = False
    def enter (self):
        announce ("You have been transported into a temple room with 3 mystic doors each varying in difficulty")

    def process_verb (self, verb, cmd_list, nouns):
        if self.incorrect:
            announce("The heavens forbid you from going back to the previous area.")
            config.the_player.next_loc = self.main_location.locations["mountain"]
            announce("you have been sent back to the mountain top")
            return
        if (verb == "south"):
            announce ("You choose to return to the mountain through the portal")
            config.the_player.next_loc = self.main_location.locations["mountain"]
        elif (verb == "west"):
            print("You arrive at door 1 the easiest door and are prompted with the question: ")
            print(f"\nWhat do both the letter T and an island have in common")
            answer = input("What is your answer?: ")
            if answer.lower() == "water":
                print("You have made the correct answer")
                announce("the gods give you sustenance as a reward")
                config.the_player.ship.food += 3
            else:
                print("your answer is incorrect")
                self.incorrect = True
                config.the_player.next_loc = self.main_location.locations["mountain"]
        elif (verb == "north"):
            print ("You arrive at door 2. THe intermediate door and are prompted with a question: ")
            print(f"\n You measure my life in hours and I serve you by expiring. I'm quick when I'm thin and slow when I'm fat. The wind is my enemy. What am I?")
            answer = input("What is your answer?: ")
            if answer.lower() == "candle":
                print("You have made the correct answer")
                announce("here is your prize")
                config.the_player.add_to_inventory([Coin()])
                config.the_player.ship.food += 3
            else:
                print("your answer is incorrect")
                self.incorrect = True
                config.the_player.next_loc = self.main_location.locations["mountain"]
        elif(verb == "east"):
            print("You arrive at the hardest door, door 3. It looks as though you are transported into a desert")
            print(f"\nyou arrive in a land of sand and are prompted with a question among the dunes and vibrant purple sky")
            print(f"\nWhat goes on four legs in the morning, on two legs by noon, and on three legs in the evening?")
            answer = input("What is your answer?: ")
            if answer.lower() == "human":
                print("You have made the correct answer")
                announce("you've been granted an incredible weapon")
                config.the_player.add_to_inventory([Ace_of_Spades()])
            else:
                print("your answer is incorrect")
                self.incorrect = True
                config.the_player.next_loc = self.main_location.locations["mountain"]
                
class King(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "king"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 100
        self.events.append(monkey_king.Monkey_King())

    def enter (self):
      announce ("You have made it to Kings Canyon, home of the feared Monkey King of the High Seas")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            print("You see the monkey kings home its a lavish overgrown castle")
        elif (verb == "north"):
            print("this area is ravaged by deforestation can't go this way")
        elif(verb == "east"):
            print("You trek back down the path from which ye came")
            config.the_player.next_loc = self.main_location.locations["jungle"]
        elif(verb == "west"):
            print("The monkey king lives on a lavish port. You look out over his coved inlet")


class Claymore(items.Item):
    def __init__(self):
        super().__init__("claymore", 60) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,80)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class Ace_of_Spades(items.Item):
    def __init__(self):
        super().__init__("Ace of Spades", 4000) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (25,100)
        self.firearm = True
        self.charges = 3
        self.skill = "guns"
        self.verb = "blast"
        self.verb2 = "blasts"

class Coin(items.Item):
    def __init__(self):
        super().__init__("Gold Coin", 2000) #Note: price is in shillings (a silver coin, 20 per pound)
