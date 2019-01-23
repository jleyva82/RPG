import random                                              #for use with .randrange(,)
from .magic import Spell


class bcolors:                                             #classes for different lettering
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:                                              #class for person / unit
    def __init__(self,name, hp, mp, atk, df, magic, items):            #set commands for each input stanciated in object call out
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):                           #function to generate attack damage
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):                           #function for unit to take damage
        self.hp -= dmg
        if self.hp < 0:                                   #safety for no hp less than 0
            self.hp = 0
        return self.hp

    def heal(self, dmg):                                   #healing function
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):                                     #call out remaing HP of unit
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):                            #function to reduce MP after use
        self.mp -= cost

    def choose_action(self):                              #function to choose appropiate action Attack or Magic
        i = 1
        print('\n' + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + 'ACTIONS:' + bcolors.ENDC)
        for item in self.action:
            print("    " + str(i) + ":", item)                      #note: convert index to string
            i += 1

    def choose_magic(self):                                #function to choose magic attack
        i = 1
        print('\n' + bcolors.OKBLUE + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print('\n' + bcolors.OKGREEN + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item["item"].name, ":", item["item"].description, "(x" + str(item["quantity"]) + ')')
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            print("        " + str(i) + ".", enemy.name)
            i += 1
        choice = int(input("    Choose target:")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ''
        bar_ticks = (self.hp / self.maxhp) * 100 / 5

        mp_bar = ''
        mp_ticks = (self.mp / self.maxhp) * 100

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 20:
            hp_bar += "_"

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1
        while len(mp_bar) < 1:
            mp_bar += "_"

        hp_string = str(self.hp) + '/' + str(self.maxhp)
        current_hp = ""
        if len(hp_string) < 11:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += ""
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""
        if len(mp_string) < 7:
            decrease = 7 - len(mp_string)

            while decrease > 0:
                current_mp += ""
                decrease -= 1

        else:
            current_mp = mp_string

        print(bcolors.BOLD + self.name + '    ' +
              hp_string + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC + bcolors.BOLD
              + "|   " +
              mp_string + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + '|')
    def get_stats(self):
        hp_bar = ''
        bar_ticks = (self.hp / self.maxhp) * 100 / 5

        mp_bar = ''
        mp_ticks = (self.mp / self.maxhp) * 100

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 20:
            hp_bar += "_"

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1
        while len(mp_bar) < 1:
            mp_bar += "_"


        hp_string = str(self.hp) + '/' + str(self.maxhp)
        current_hp = ""
        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += ""
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""
        if len(mp_string) < 7:
            decrease = 7 - len(mp_string)

            while decrease > 0:
                current_mp += ""
                decrease -= 1

        else:
            current_mp = mp_string

        print(bcolors.BOLD + self.name + '    ' +
              hp_string + "   |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + bcolors.BOLD
              + "|   " +
              mp_string + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + '|')
