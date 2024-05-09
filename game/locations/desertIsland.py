#Kevin's Island

from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu
import game.superclasses as superclasses

class DesertIsland(location.Location):

    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "desert island"
        self.symbol = 'DI'
        self.visitable = True
        self.starting_location = SandCoast(self)
        self.locations = {}

        self.locations['sandCoast'] = SandCoast(self)
        self.locations['entranceRoom'] = EntranceRoom(self)
        self.locations['burialChamber'] = BurialChamber(self)
        self.locations['throneRoom'] = ThroneRoom(self)
        self.locations['treasureRoom'] = TreasureRoom(self)

    def enter(self, ship):
        print('You have arrived a scorching desert island.')

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        

class SandCoast(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "sand coast"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self):
        pirates = config.the_player.get_pirates()
        for pirate in pirates:
            pirate.inflict_damage(2, " hot sand.")
        announce('You arrive on the desert. The hot sand burn at your feet.')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["entranceRoom"]
        elif (verb == "east" or verb == "west"):
            announce ("You walk all the way around the island on the desert coast. The hot sand hurts your feet.")


class EntranceRoom(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "entrance room"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self

        self.event_chance = 100
        self.events.append(MummieAttackEvent())
    
    def enter(self):
        announce('You reach the entrance of the palace on the desert.')
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["sandCoast"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["burialChamber"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["throneRoom"]

class MummieAttackEvent(event.Event):
    def __init__(self):
        self.name = ' a group of mummies attack.'

    def process(self, world):
        result = {}
        result["message"] = "The mummies disolve into a pile of bandages"
        mummies = []
        n_appearing = random.randrange(3,5)
        n = 1
        while n <= n_appearing:
            mummies.append(MummieAttack("Guardian Mummy "+str(n)))
            n += 1
        announce("A group of mummies turn towards your crew and attack!")
        combat.Combat(mummies).combat()
        result["newevents"] = []

        return result

class MummieAttack(Monster):
    def __init__(self, name):
        attacks = {}
        attacks['punch'] = ["punches", random.randrange(30, 45), (15,21)]
        attacks['strangle'] = ["strangles", random.randrange(60, 95), (5,11)]
        super().__init__(name, random.randrange(7, 35), attacks, 60 + random.randrange(-20, 20))


class BurialChamber(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "burial chamber"
        self.verbs['south'] = self

        #Items to pick up in the burial chambers
        self.verbs['take'] = self
        self.item_on_coffin = items.Cutlass()
        self.item_on_skeleton = items.Flintlock()
        self.item_on_floor = Treasure()

    def enter(self):
        description = 'You enter burial chamber of the palace.'

        #Announcing both items
        if self.item_on_coffin != None:
            description = description + "\nYou see a " + self.item_on_coffin.name + " thrusted inside a sarcophagus. \n An dark aura pulses from the blade."
        if self.item_on_skeleton != None:
            description = description + "\nYou see a skeleton on the ground holding a " + self.item_on_skeleton.name + "."
        if self.item_on_floor != None:
            description = description + "\nYou see a pile of " + self.item_on_floor.name +" on the ground."
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["entranceRoom"]
        
        if verb == "take":
            if self.item_on_skeleton == None and self.item_on_coffin == None and self.item_on_floor == None:
                announce ("You don't see anything to take.")
            elif  len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                #Cutlass pick option + random crewmate gets sick
                item = self.item_on_coffin
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    description = "You take the " + item.name + " from the sarcophagus. "
                    randomPirate = random.choice(config.the_player.get_pirates())
                    randomPirate.set_sickness (True)
                    description += randomPirate.name + " got sick due to the corpse's curse. \n Open..."
                    config.the_player.add_to_inventory([item])
                    self.item_on_coffin = None
                    config.the_player.go = True
                    at_least_one = True
                    announce(description)
                #Pistol pick option
                item = self.item_on_skeleton
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the " + item.name + " out of the skeleton's hand. ...It looks like he failed to escape from something. \n ...door")
                    config.the_player.add_to_inventory([item])
                    self.item_on_skeleton = None
                    config.the_player.go = True
                    at_least_one = True
                #Treasure pick option   
                item = self.item_on_floor
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the " + item.name + " off the ground. It will be worth a lot if you survive.")
                    config.the_player.add_to_inventory([item])
                    self.item_on_floor = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")


class Treasure(items.Item):
    #a item that only serves as more shillings
    def __init__(self):
        super().__init__("treasure", 5000)
        

class ThroneRoom(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "throne room"
        self.verbs['north'] = self
        self.verbs['east'] = self
        self.verbs['open'] = self
        self.open = False
    
    def enter(self):
        description = 'You enter the throne room of the palace.'
        if (self.open == False):
            description += " The throne looks crooked."
        else:
            description += " The throne is moved to the side."
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north" and self.open == True):
            config.the_player.next_loc = self.main_location.locations["treasureRoom"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["entranceRoom"]
        if (verb == "open"):
            if  len(cmd_list) > 1:
                if (cmd_list[1] == "door"):
                    self.open = True
                    announce("You move the throne aside to reveal a secret entrance, you can now head north.")
            else:
                announce("What do you want to open?")

class TreasureRoom(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "treasure room"
        self.verbs['south'] = self

        self.verbs['take'] = self
        self.item = StaffofLife()

        self.event_chance = 100
        self.events.append(SphynxEvent())

    def enter(self):
        description = 'You enter treasure room of the palace.'
        if self.item != None:
            description = description + "\nYou see a " + self.item.name +" on the ground."
        announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["throneRoom"]
        if verb == "take":
            if self.item == None:
                announce ("You don't see anything to take.")
            elif  len(cmd_list) > 1:
                at_least_one = False 
                item = self.item
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all" or cmd_list[1] == "staff"):
                    announce ("You pick up the " + item.name + " out off the ground. You instinctively undertstand that the staff will help once per day.")
                    config.the_player.add_to_inventory([item])
                    self.item = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")


class SphynxEvent(event.Event):
    '''The boss of the island, if you gets its riddles right, 
    it  will not bother you, other wise boss fight'''
    def __init__(self):
        self.name = " the guardian of the pyrimad strikes"
        self.wins = 0
        self.losses = 0
        self.round = 0
        
    def process(self, world):
        sphynx = SphynxBoss()
        result = {}
        description = "A massive Sphynx stands before you."
        description += "\nSphynx: If you wish to pass unharmed, you must best me in 3 game of rock-paper-sicssor\nIf you lose twice, well you'll see..."
        announce(description)
        if self.riddles(): 
            message = "The sphynx fades away"
        else:
            message = 'The sphynx crumbles away'
            announce("The sphynx attacks")
            combat.Combat([sphynx]).combat()        
        
        result["message"] = message
        result["newevents"] = []
        return result

    def riddles(self):
        while (self.wins < 3 and self.losses < 2):
            self.round += 1
            announce(f'\nCurrent Round: {self.round}, Wins: {self.wins}, Losses: {self.losses}')
            answer = input("a - Rock \nb - Paper \nc - Scissor \nMake a selection: ")
            choice = random.randint(1, 3) #1 is rock, 2 is paper, 3 is scissor
            if choice == 1:
                description = 'rock'
            elif choice == 2:
                description = 'paper'
            else:
                description = 'scissor'
            
            if (answer != 'a' and answer != 'b' and answer != 'c'):
                announce("Select one of the three")
                self.round -= 1

            announce('Sphynx picked ' + description)
            if (choice == 1 and answer == 'a') or  (choice == 2 and answer == 'b') or (choice == 3 and answer == 'c'):
                announce("You picked the same choice, again")
            elif (choice == 1 and answer == 'c') or  (choice == 2 and answer == 'a') or (choice == 3 and answer == 'b'):
                announce("You lose")
                self.losses +=1
            else:
                announce("You win")
                self.wins +=1
  
        if self.wins >= 3:
            return True
        elif self.losses >=2:
            return False
            

class SphynxBoss(Monster):
    def __init__(self):
        attacks = {}
        attacks['scratch'] = ["scratches", random.randrange(80, 95), (10, 15)]
        attacks['bite'] = ["bites", random.randrange(35, 70), (20, 35)]
        super().__init__('Great Sphynx', random.randrange(400, 650), attacks, 250 + random.randrange(-40, 40))    
   
    def getAttacks(self):
        specialAttack = superclasses.specialAttack('Magic', 'curses')
        attacks = []
        for key in self.attacks.keys():
            attack = superclasses.Attack(key, self.attacks[key][0], self.attacks[key][1], self.attacks[key][2], False)
            attacks.append(superclasses.CombatAction(attack.name, attack, self))
        attacks.append(superclasses.CombatAction(specialAttack.name, specialAttack, self))
        return attacks

    def pickAction(self):
        attacks = self.getAttacks()
        return random.choice(attacks)

        
    

class StaffofLife(items.Item):
    '''Once per day this staff can heal the crewmates up to 3 times their regeneration and remove any sickness '''
    def __init__(self):
        super().__init__("staff of life", 1000)
        self.skill = "healing"
        self.verb = "heals"

def check_inventory():
    status = False
    for item in config.the_player.inventory:
        if item.name == "staff of life":
            status = True

    if status == True:
        return True
