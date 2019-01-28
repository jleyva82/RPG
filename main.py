'''
Author: Jesus Leyva
What: RPG Battle Script
Date of Last Update: 01/27/2019
Area's to Improve:
    Better Enemy AI
    Trouble Shoot HP and MP Bars
    Character Balance
'''

#Import Classes
from classes.game import Person, bcolors
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

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_magic = [fire, thunder, blizzard, meteor, cure]

#create some items
potion = Item("Potion", "potion", "Heals 50 HP", 250)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 500)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one pa1rty member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 1000 damage", 1000)


player_items = [{'item': potion, "quantity": 15},
                {'item': hipotion, 'quantity': 5},
                {'item': superpotion, 'quantity': 5},
                {'item': elixer, 'quantity': 5},
                {'item': hielixer, 'quantity': 2},
                {'item': grenade, 'quantity': 5}]

enemy_items = [{'item': potion, "quantity": 5},
                {'item': hipotion, 'quantity': 2},
                {'item': elixer, 'quantity': 1}]

#instatiate people
player1 = Person("Valos", 3260, 132, 300, 34, player_magic, player_items)
player2 = Person("Nick ", 4160, 188, 311, 34, player_magic, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_magic, player_items)

enemy1 = Person("Magus", 11200, 701, 525, 25, enemy_magic, enemy_items)
enemy2 = Person("Magot", 1250, 130, 560, 325, enemy_magic, enemy_items)
enemy3 = Person("Magot", 1250, 130, 560, 325, enemy_magic, enemy_items)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True                                                 #make sure it runs and have initial index
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)                 #imitiate battle

while running:                                                 #create running battle loop
    #User UI with HP and MP Bars
    print("====================")
    print("NAME                   HP                                       MP")
    for player in players:
        player.get_stats()                                     #uses get_stats function for individual player stats
    print('\n')
    for enemy in enemies:
        enemy.get_enemy_stats()                                #uses get_stats function for indivisual enemies

    #players turn
    for player in players:
        player.choose_action()
        choice = input("Choose action")                            #take user input for action
        index = int(choice) - 1                                    #decrease by one for proper python indexing

        #player attacks
        if index == 0:                                             #suppose that player chooses attack
            dmg = player.generate_damage()                         #generate damage caused by player
            enemy = player.choose_target(enemies)                  #player chooses target

            enemies[enemy].take_damage(dmg)                                 #enemy takes damage
            print(player.name, "attacks", enemies[enemy].name, "for", dmg, "points of damage.")     #user info

            if enemies[enemy].get_hp() == 0:                        #user info, enemy death
                print(bcolors.FAIL + bcolors.BOLD + enemies[enemy].name, "has died." + bcolors.ENDC)
                if enemies[0].get_hp() == 0:                        #exit loop if boss has died
                    print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                    break
                del enemies[enemy]                                   #delete enemy from party

        #player uses magic
        elif index == 1:
            player.choose_magic()                                    #User UI, magic selection
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:                                   #go back
                continue

            spell = player.magic[magic_choice]                       #instantiate players magic choice
            magic_dmg = spell.generate_damage()                      #generate magic damage

            current_mp = player.get_mp()                             #identify current mp levels

            if spell.cost > current_mp:                              #what if not enough mp for magic
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)                             #reduce cost of mp used in spell

            #Healing Magic
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            #Attack Magic
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:                       #player UI, enemy death
                    print(bcolors.FAIL + bcolors.BOLD + enemies[enemy].name, "has died." + bcolors.ENDC)
                    if enemies[0].get_hp() == 0:                       #player UI, Boss Death
                        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                        break
                    del enemies[enemy]

        #player choose items
        elif index == 2:
            player.choose_item()                                       #player UI, item menu
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:                                      #go back
                continue

            item = player.items[item_choice]["item"]                   #instantiate item

            if player.items[item_choice]["quantity"] == 0:             #player UI, not enough items
                print(bcolors.FAIL + '\n' + "None left ..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1                 #item usage


            #item types
            #healing items
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":                           #do this for all members of player party
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp                            #regen HP and MP for individual player
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + '\n' + item.name + " fully restore HP/MP" + bcolors.ENDC)
            #damage items
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop) + " point of damage to " +
                      enemies[enemy].name + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + enemies[enemy].name, "has died." + bcolors.ENDC)
                    if enemies[0].get_hp() == 0:
                        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                        break
                    del enemies[enemy]

    if enemies[0].get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    print('\n')
#new code for enemy AI
#enemy's turn
    if enemies[0].get_hp() != 0:
        for enemy in enemies:                                        #generate action for enemies
            #enemy.choose_action()
            index = random.randrange(0, 2)


            if index == 0:                                             #suppose that player chooses attack
                dmg = enemy.generate_damage()                            #generate damage
                enemy_target = int(random.randrange(0, 3))
                player = enemy_target

                players[player].take_damage(dmg)                                 #player takes damage
                print(enemy.name, "attacks", players[player].name, "for", dmg, "points of damage.")     #user info

                if players[player].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + players[player].name, "has died." + bcolors.ENDC)
                    #del players[player]     #do I want to delete the player??

            elif index == 1:
                #enemy.choose_magic()
                magic_choice = random.randrange(0,5)

                #if magic_choice == -1:
                 #   continue

                spell = enemy.magic[magic_choice]
                magic_dmg = spell.generate_damage()

                current_mp = enemy.get_mp()

                if spell.cost > current_mp:
                    print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                    continue

                enemy.reduce_mp(spell.cost)

                if spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(bcolors.OKGREEN + enemy.name + " uses " + spell.name + " to heal for", str(magic_dmg), "HP." + bcolors.ENDC)
                elif spell.type == "black":
                    enemy_target = int(random.randrange(0, 3))
                    player = enemy_target
                    players[player].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + enemy.name + " uses " + spell.name + " to deal", str(magic_dmg), "points of damage to " +
                          players[player].name + "." +  bcolors.ENDC)

                    if players[player].get_hp() == 0:
                        print(bcolors.FAIL + bcolors.BOLD + players[player].name, "has died." + bcolors.ENDC)
                        #del enemies[enemy]                   #do I want to delete players???

            elif index == 2:
                #enemy.choose_item()
                item_choice = random.randrange(0, 3)

                #if item_choice == -1:
                 #   continue

                item = enemy.items[item_choice]["item"]

                if enemy.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + '\n' + "None left ..." + bcolors.ENDC)
                    continue

                enemy.items[item_choice]["quantity"] -= 1


                if item.type == "potion":
                    enemy.heal(item.prop)
                    print(bcolors.OKGREEN + '\n' + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
                elif item.type == "elixer":
                    if item.name == "MegaElixer":
                        for i in enemies:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        enemy.hp = enemy.maxhp
                        enemy.mp = enemy.maxmp
                    print(bcolors.OKGREEN + '\n' + item.name + " fully restore HP/MP" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy_target = int(random.randrange(0, 3))
                    player = enemy_target
                    players[player].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop) + " point of damage to " +
                          players[player].name + bcolors.ENDC)

                    if players[player].get_hp() == 0:
                        print(bcolors.FAIL + bcolors.BOLD + players[player].name, "has died." + bcolors.ENDC)
                        #del players[player]            #do I want to delete the player???


    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    defeated_enemies = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if enemies[0].get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False
