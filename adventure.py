"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed


def move(p: Player, location: Location, choice: str) -> None:
    if choice not in location.available_actions():
        print("Sorry! You can't go that way!")
    elif choice == 'N':
        p.y -= 1
    elif choice == 'S':
        p.y += 1
    elif choice == 'W':
        p.x -= 1
    elif choice == 'E':
        p.x += 1


def do_action(w: World, p: Player, location: Location, choice: str) -> None:
    if choice == "look":
        print(location.long)
    elif choice == "inventory":
        cur_inventory = [item.name for item in p.inventory]
        if not cur_inventory:
            print("Hmm, it seems that you have nothing in your inventory.")
        else:
            print("Here are the items you have in your inventory:")
            print(cur_inventory)
        for item in w.items:
            if item.current_location == location.num:
                get_item = ''
                while get_item != 'y' and get_item != 'n':
                    get_item = input("There is a " + item.name + " at this location. Would you like to add it to your inventory? [y/n]")
                if get_item == 'y':
                    p.inventory.append(item)
                    item.current_location = -1

        drop_item = input("Would you like to drop an item here? [y/n]")
        while drop_item != 'y' and drop_item != 'n':
            drop_item = input("Sorry, please enter 'y' or 'n'. Would you like to drop an item here? [y/n]")
        while drop_item == 'y':
            to_be_dropped = input("What would you like to drop? Please type the name exactly as it is displayed.")
            if to_be_dropped in cur_inventory:
                for item in p.inventory:
                    if item.name == to_be_dropped:
                        p.inventory.remove(item)
                        item.current_location = location.num
            drop_item = input("Would you like to drop another item here? [y/n]")

    elif choice == "score":
        t = 0
    elif choice == "quit":
        t = 0
    elif choice == "back":
        t = 0
    else:
        t = 0


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(1, 3)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]

    while not p.victory:
        location = w.get_location(p.x, p.y)

        if location.visits > 0:
            print(location.short)
        else:
            print(location.long)
        location.visits += 1

        print("What to do? \n")
        print("[menu]")
        for action in location.actions:
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            do_action(w, p, location, choice)

        move(p, location, choice)

        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
