from classes.game import Person, bcolors                       #import appropiate classes
from classes.magic import Spell
from classes.inventory import Item
import random


#create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 30, 1140, "black")

#create white magic
cure = Spell("Cure", 20, 600, "white")
cura = Spell("Cura", 25, 1500, "white")

#create some items
potion = Item("Potion", "potion", "Heals 50 HP", 250)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 500)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one pa1rty member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 1000)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{'item': potion, "quantity": 15},
                {'item': hipotion, 'quantity': 5},
                {'item': superpotion, 'quantity': 5},
                {'item': elixer, 'quantity': 5},
                {'item': hielixer, 'quantity': 2},
                {'item': grenade, 'quantity': 5}]

#instatiate people
player1 = Person("Valos", 3260, 132, 300, 34, player_magic, player_items)                     #create players and enemy
player2 = Person("Nick ", 4160, 188, 311, 34, player_magic, player_items)                     #create players and enemy
player3 = Person("Robot", 3089, 174, 288, 34, player_magic, player_items)                     #create players and enemy

enemy1 = Person("Magus", 11200, 701, 525, 25, [], [])
enemy2 = Person("Magot", 1250, 130, 560, 325, [], [])
enemy3 = Person("Magot", 1250, 130, 560, 325, [],[])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True                                                 #make sure it runs and have initial index
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)                 #UI imitiate battle

while running:                                                 #create running battle loop
    print("====================")
    print("                      NAME                                       MP")
    for player in players:
        player.get_stats()
    print('\n')
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action")                            #take user input for action
        index = int(choice) - 1                                    #decrease by one for proper python indexing

        if index == 0:                                             #suppose that player chooses attack
            dmg = player.generate_damage()                      #generate damage caused by player
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)                                 #enemy takes damage
            print(player.name + " attacked" + enemies[enemy].name + "for", dmg, "points of damage.")     #user info

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + '\n' + "None left ..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + '\n' + item.name + " fully restore HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop) + " point of damage to " + enemies[enemy].name + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemies[0].generate_damage()                                                       #generate damage caused by enemy
    target = random.randrange(0,3)
    players[target].take_damage(enemy_dmg)                                                    #player takes damage
    print("Enemy attacks for", enemy_dmg, "points of damage.")                                #user info

    if enemies[0].get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player1.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False