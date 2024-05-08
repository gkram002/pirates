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
import game.player as player

'''
Code for the debug position of the island, if in use this would be placed in 'world.py'

# My Island, directly to the left of the spawning location
        abandonedIsle = abandonedIsland.AbandonedIsland(self.startx - 1, self.starty, self)
        self.locs[self.startx - 1][self.starty] = abandonedIsle
'''



class AbandonedIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'A'
        self.visitable = True

        self.button_puzzle = ButtonPuzzle()

        self.starting_location = Beach_with_ship(self)
        self.locations = {}

        self.locations["southBeach"] = self.starting_location
        self.locations["northBeach"] = NorthBeach(self)
        self.locations["westBeach"] = WestBeach(self)
        self.locations["eastBeach"] = EastBeach(self)

        self.locations["hill"] = Hill(self)
        self.locations["livingStatues"] = LivingStatues(self)
        self.locations["church"] = Church(self)

    def enter (self, ship):
        print ("You have arrived at an abandoned island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

# Beach location classes
class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.rock_number = m.button_puzzle.get_number(self.name[0])

        # All beaches have a 25% chancce for a seagull encounter
        self.event_chance = 25
        self.events.append (seagull.Seagull())

        # Possible future event ideas, not going to add them in initial island release though.
        #self.events.append (crate.Crate()) # Idea for an event where the user finds a washed up crate on the shore)
        #self.events.append (octopus.Octopus()) # Random Idea I had for an event, an octopus attack

    def enter (self):
        announce ("\nYou arrive at the south side of the island, on a beach. Your ship is at anchor in a small bay to the south." + 
                  "\nThere is a small hill to the north. It has some sort of ruins on it." +
                  f"\nA little further down the beach you see a rock formation that is oddly shaped like the number {self.rock_number}")

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

        self.rock_number = m.button_puzzle.get_number(self.name[0])

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = ("\nArriving on the East side of the island, there isn't much to see other than another weird rock formation and some seagulls." +
                       f"\nThis time the rock is in the shape of the number {self.rock_number}.")
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        elif (verb == "south" or verb == "north"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]

class WestBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.rock_number = m.button_puzzle.get_number(self.name[0])

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = ("\nYou arrive on the Westmost side of the island, which has some scattered palm trees and a nice cool breeze blowing over it." +
                       f"\nWhile looking around the beach, you discover another large rock formation in the shape of a {self.rock_number}.")
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        elif (verb == "south" or verb == "north"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]

class NorthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.m = m
        self.name = "northBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['investigate'] = self

        self.rock_number = m.button_puzzle.get_number(self.name[0])

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = ("\nYou arrive at the Northmost side of the island, which has sparse amounts of beach grass growing along it." + 
                       "\nStrangely, there is a large stone platform in the middle of the beach." +
                       f"\nNear the platform there is another one of those rocks, this time shaped like a {self.rock_number}.")
        announce(description)
        announce("\nThe oddity of a stone platform on a beach entices you to investigate it.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["hill"]
        elif (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
        elif (verb == "investigate"):
            announce("\nUpon investigating the stone platform, it appears there is a locked stone chest in the center of it, with 4 large buttons set into the stone." +
                 "\nThe north button is marked with an N, West with a W, South with an S, and East with an E." +
                 "\n\nOn the chest there appears to be remnants of a message:" +
                 "\n\tPr--s -he but--n- in th- -or-ect ord-r to gai- a-c-ss to --e tr-as--e wit--n.")
            self.start_puzzle()
            
    
    def start_puzzle(self):
        decision = input("\nDo you want to try to solve the puzzle? ")
        try:
            if decision[0] == 'y':
                self.m.button_puzzle.button_presses()
            else:
                print("Choosing to not attempt the puzzle, you rest on the beach.")
        except:
            print("Choosing to not attempt the puzzle, you rest on the beach.")

# Class for the Hill location
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
        description = ("\nYou reach the crest of the small hill after walking for some time." +
                       "\nBefore you lies a long-abandoned church with three tall statues to the side of its doors." + 
                       "\n\nYou wonder what you would find if you were to enter the church or investigate the statues.")

        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
        elif (verb == "enter"):
            if self.main_location.locations["church"].door_check():
                config.the_player.next_loc = self.main_location.locations["church"]
                config.the_player.go = True
            else:
                print("You try to open the doors to the church, but they won't budge.")
        
        elif (verb == "investigate"):
            config.the_player.next_loc = self.main_location.locations["livingStatues"]
            config.the_player.go = True

# Class for the Living Statues
class LivingStatues (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = 'livingStatues'
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['enter'] = self
        self.verbs['investigate'] = self
    
    def enter (self):
        description = "\nYou walk up to the statues, and to your surprise, they start talking to you."
        announce(description)
        self.HandleStatues()

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
        elif (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations[f"hill"]
            config.the_player.go = True
        elif (verb == "enter"):
            if self.main_location.locations["church"].door_check():
                config.the_player.next_loc = self.main_location.locations["church"]
                config.the_player.go = True
            else:
                print("You try to open the doors to the church, but they won't budge.")
        elif (verb == "investigate"):
            self.enter()

    def HandleStatues(self):
        print("\nStatue 2: Hello there travellers!")
        print("Statue 1: Welcome to the island!")
        announce("Statue 3: If you wish to enter that old church and seek salvation, you must correctly answer our Knights and Knaves riddle!")

        choice = input("Statue 2: Would you like to answer our riddle? ")
        if len(choice) == 0:
            print("\nStatues: Safe adventures, travellers!")
            print("The statues become dormant once again.")
        elif choice[0].lower() == 'y':
            self.HandleRiddle()
        else:
            print("\nStatues: Safe adventures, travellers!")
            print("The statues become dormant once again.")

        announce("\nYou may now leave the statues, investigate them again, head to another part of the island, or enter the church if the doors have opened.")

    def HandleRiddle(self):
        '''Handles the statues' Knights & Knaves riddle.'''
        riddle = self.GetRiddleAndAnswer()
        self.guesses = 3

        # While the player still has guesses, ask for their answer and respond appropriately.
        while self.guesses > 0:
            self.PrintRiddle(riddle)
            plural = ""
            if(self.guesses != 1):
                plural = "s"
            
            print(f"\nYou may guess {self.guesses} more time{plural}.") 
            
            guess_string = self.RiddleGuess()

            if riddle[3] in guess_string:
                self.main_location.locations["church"].set_open()
                announce("\nThe doors to the church swing open.")
                announce("Statues: Congratulations! You have answered our riddle correctly!")
                return
            elif len(riddle) > 4:
                # This is in case there happens to be a second answer to the Knights & Knaves puzzle.
                if riddle[4] in guess_string:
                    self.main_location.locations["church"].set_open()
                    announce("\nThe doors to the church swing open.")
                    announce("Statues: Congratulations! You have answered our riddle correctly!")
                    return
            self.guesses -= 1
            announce("Statues: You have guessed incorrectly.")

        # After user runs out of guesses this is printed
        print("Statues: Sorry, you ran out of guesses, come back later!")
        return

    def GetRiddleAndAnswer(self):
        '''Returns a random knights & knaves riddle.'''
        riddleList = [ # A list of tuples. The first three items are the dialogue for each statue, and the remaining items are the possible answers.
            ("Statue 2 is a truthteller", "Statue 3 is a liar", "Statue 1 is a liar", "T, T, F", "F, F, T"),
            ("Statues 2 and 3 are liars", "Statue 1 is a truthteller", "Statue 2 is a liar", "F, F, T"),
            ("Statue 3 is a liar", "Statues 1 and 3 are not the same", "Statue 2 is a truthteller", "F, T, T")
            ]
        return random.choice(riddleList)
        
    def PrintRiddle(self, riddle):
        '''Prints the riddle.'''
        print(f"\nStatue 1: {riddle[0]}")
        print(f"Statue 2: {riddle[1]}")
        print(f"Statue 3: {riddle[2]}")
    
    def RiddleGuess(self):
        '''Handles the guesses for each statue, stores them in order in a list'''
        guesses = []
        print("For your guesses, put T if the statue is a Knight (their statement is true) and F if the statue is a Knave (their statement is false).")
        for i in range(1,4):
            guess = input(f"What is your guess for Statue {i}? ")
            guesses.append(guess)

        # Formatting the guesses into a single answer
        return f"{guesses[0]}, {guesses[1]}, {guesses[2]}".upper()
    
# Class for the Church location
class Church (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = 'Old Church'
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['investigate'] = self
        self.verbs['search'] = self

        self.inside = False
        self.shrineUsed = False
        self.open = False
        self.pot_full = True
    
    def enter (self):
        if not self.inside:
            description = ("\nRemnants of benches and other debris are scattered about the room." +
                            "\nYou can see a pot in the corner to the left of the entrance, next to two large sets of armor." +
                            "\nLooking up, there is a hole in the roof that sunlight is shining through, illuminating an altar towards the front of the sanctuary." + 
                            "\nLooming above the altar is a dark shrine, seemingly unaffected by time and shadowed despite being in direct light.")
            announce(description)
            announce("\nSomething about the altar and shrine beckons you to investigate them. There could also be something in the pot, so it would be wise to search it.")
        self.inside = True
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'exit' or verb == 'leave'):
            config.the_player.next_loc = self.main_location.locations['hill']
            self.inside = False
            config.the_player.go = True
        elif (verb == 'search'):
            if self.pot_full == True:
                self.pot()
            else:
                announce("The pot is empty.")
        elif (verb == 'investigate'):
            if self.shrineUsed == False:
                announce("As you approach the altar and shrine, the shrines's eyes suddenly start glowing red...")
                self.altar()
            else:
                announce("The shrine lies dormant.")
    
    def pot(self):
        '''Contains a necklace worth 10 shillings and some food.'''
        num = random.randint(20,40)
        print(f"Inside the pot you find {num} food, and an old necklace, which you take.")
        config.the_player.ship.food += num
        config.the_player.add_to_inventory([OldNecklace()])

        # Change the pot to being empty
        self.pot_full = False

    def set_open(self):
        '''Sets the church doors to be open'''
        self.open = True
        return
    
    def door_check(self):
        '''Returns the state of the church doors, whether they are open or not.'''
        return self.open
    
    def altar(self):
        '''Demonic shrine & altar. Player can choose to make a sacrifice in order to increase other player's stats, or attempt to leave and get attacked.'''
        announce("Dark Shrine: Welome... mortals.")
        announce("Dark Shrine: I offer you an increase in all your skills, for a small price.")
        announce("Dark Shrine: A SACRIFICE!")
        decision = input("\nDark Shrine: So, what'll it be then? Will you make a sacrifice? (if so, enter yes) ")
        if decision.lower() == 'yes':
            self.sacrifice()
            self.shrineUsed = True
        else:
            announce("\nDark Shrine: Oh, no? That's fine I guess.")
            announce("Dark Shrine: Watch out for the guards on your way out!")
            self.event_chance = 100
            self.events.append(PhantomArmorEvent())
            config.the_player.go = True
            
    def sacrifice(self):
        '''Sacrifices one of the pirates (at random) to the shrine, and increases the stats of the other pirates.'''
        # Get a list of the pirates, choose a random one, sacrifice them, say they were sacrificed, adjust stats of other pirates.
        pirates = player.Player.get_pirates(config.the_player)
        if len(pirates) > 1:
            num = random.randint(0,len(pirates)-1)
            pirates[num].kill(deathcause="Sacrificed")
            announce(f"\n{pirates[num].name} has been sacrificed!")

            pirates.remove(pirates[num])
        else:
            announce("Dark Shrine: Why would you choose sacrifice? There's only one of you left...")
            announce("Dark Shrine: Well, I don't kill parties, only burden them.")
            announce("Dark Shrine: Good bye and good luck, lonesome traveller!")
            print("The shrine goes quiet, and you are left in complete silence")
            return 
        
        # Boost player stats (I left the testing stuff in there commented out on purpose, thought it was cool to see the number adjustments. Yes I'm a nerd.)
        for p in pirates:
            #print(f"Before Boost: {p.skills}")
            p.skills["brawling"] += random.randrange(10,25)
            p.skills["swords"] += random.randrange(10,25)
            p.skills["melee"] += random.randrange(10,25)
            p.skills["guns"] += random.randrange(10,25)
            p.skills["cannons"] += random.randrange(10,25)
            p.skills["swimming"] += random.randrange(10,25)
            #print(f"After boost: {p.skills}")
            for skill in p.skills:
                if p.skills[skill] > 100:
                    p.skills[skill] = 100
            #print(f"After fixing: {p.skills}")

        print("\nDark Shrine: Thank you dear travellers, for that precious soul...")
        print("The shrine goes quiet, and you are left in complete silence, appalled by what just happened to your fellow pirate, yet feeling stronger.")

# Classes for the Phantom Armor Guard combat event
class PhantomArmorEvent (event.Event):
    '''Phantom Armor Guards for when the player tries to leave the church on the abandoned island without making a sacrifice to the dark shrine.'''
    def __init__ (self):
        self.name = " phantom armor attack"

    def process (self, world):
        '''Process the event. Populates a combat with 2 Phantom Armor sets.'''
        result = {}
        result["message"] = "the guards have been defeated!"

        guards = []
        guards.append(Guard("Guard 1"))
        guards.append(Guard("Guard 2"))

        announce ("You turn to leave but are attacked by two Phantom Armor Guards!")
        combat.Combat(guards).combat()
        result["newevents"] = []

        return result

class Guard(Monster):
    '''Phantom Armor Guard that attacks if you do not sacrifice someone to the dark shrine in the church.'''
    # Phantom Armor / Guard can slash, punch, or kick. Slashing does more damage than punching or kicking.
    # 120-200 hp, 100 to 140 speed (100 is "normal")
    
    def __init__ (self, name):
        attacks = {}
        attacks["slash"] = ["slashes",random.randrange(80,90), (15,25)]
        attacks["punch"] = ["punches",random.randrange(70,80), (10,18)]
        attacks["kick"] = ["kicks",random.randrange(70,80), (10,18)]
        super().__init__(name, random.randrange(120,201), attacks, 100 + random.randrange(41))

# Class to handle the button puzzle
class ButtonPuzzle:
    def __init__(self):
        '''Initialize the number on each of the beaches. This is randomized so the puzzle is different each time.'''
        self.puzzle_solved = False
        self.create_solution_string()

    def create_solution_string(self):
        '''Creates the solution string for the order the buttons need to be pressed in.'''
        num_list = [1, 2, 3, 4]
        beach_list = ['n','s','e','w']
        self.beach_numbers = {}

        for i in range(0,4):
            choice = random.randint(0,len(num_list)-1)
            beach_num = num_list[choice]
            self.beach_numbers[beach_list[i]] = beach_num

            num_list.remove(beach_num)
        
        sorted_beach_numbers = dict(sorted(self.beach_numbers.items(), key=lambda x:x[1]))
        indexes = []

        for key in sorted_beach_numbers.keys():
            index = f'{key}'
            indexes.append(index)

        self.solution_string = f'{indexes[0]}, {indexes[1]}, {indexes[2]}, {indexes[3]}'

    def get_number(self, beach):
        '''Returns the number that is on the given beach.
        The input value for beach is the first letter of the beach's name, so it corresponds to the key in the dictionary.'''

        return self.beach_numbers[beach.lower()]

    def button_presses(self):
        '''When the player is at the north beach, they can attempt to solve the NESW button puzzle, which triggers this function.'''
        if self.puzzle_solved == False:
            print("When entering which buttons you press, enter N, E, S, or W for the corresponding button.")
            button1 = input(f"Press the first button: ")
            button2 = input(f"Press the second button: ")
            button3 = input(f"Press the third button: ")
            button4 = input(f"Press the fourth button: ")

            try:
                guess_string = f"{button1[0]}, {button2[0]}, {button3[0]}, {button4[0]}"
                if guess_string.lower() == self.solution_string:
                    self.puzzle_solved = True
                    self.reward()
                else:
                    announce("Nothing happened, maybe the buttons were pressed in the wrong order?")
                    self.try_again()
            except:
                announce("Nothing happened, maybe you didn't press one of the buttons properly and it didn't count it.")
                self.try_again()
        else:
            print("This puzzle has already been solved.")
    
    def try_again(self):
        decision = input("Try again? ")
        try:
            if decision[0].lower() == 'y':
                self.button_presses()
            else:
                print("Deciding to not reattempt the puzzle, you rest on the beach.")
        except:
            print("Deciding not to reattempt the puzzle, you rest on the beach.")

    def reward(self):
        '''If the user correctly completes the puzzle, this function is triggered.'''
        # The reward is a shiny Rubik's cube worth 25 shillings, it is inside the locked chest at the center of the platform

        print("\nYou hear a low rumble and a turning of gears from inside the platform, and suddenly, with a loud 'click', the chest opens.")
        announce("Inside is a note:\n\t\"Congratulations! You have solved the puzzle! Your reward is a shiny Rubik's cube!\"")
        announce("\nYou grab the shiny Rubik's cube and then rest on the beach, since there is now nothing else to do here.")
        config.the_player.add_to_inventory([ShinyRubiksCube()])

# Classes for items made specifically for this island
class ShinyRubiksCube(Item):
    '''Rubik's Cube item. Obtained after completing the Button Puzzle.'''
    def __init__(self):
        super().__init__("shiny rubik's cube", 25) 

class OldNecklace(Item):
    '''Old Necklace item. Found in a pot inside the old church.'''
    def __init__(self):
        super().__init__("old necklace", 10)