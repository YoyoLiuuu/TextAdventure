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
import sys

# Note: You may add helper functions, classes, etc. here as needed


def move(p: Player, location: Location) -> None:
    if p.choice not in location.available_actions():
        print("Sorry! You can't go that way!")
    elif p.choice == 'N':
        p.y -= 1
    elif p.choice == 'S':
        p.y += 1
    elif p.choice == 'W':
        p.x -= 1
    elif p.choice == 'E':
        p.x += 1
    p.previous_actions.append(p.choice)
    p.total_moves += 1


def do_action(w: World, p: Player, location: Location) -> None:
    if p.choice == "look":
        print(location.long)
    elif p.choice == "inventory":
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
        if cur_inventory:
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
                            if item.target_position == location.num and not item.point_scored:
                                p.score += item.target_points
                                item.point_scored = True
                drop_item = input("Would you like to drop another item here? [y/n]")

    elif p.choice == "score":
        print("You currently have " + str(p.score) + " points. The maximum amount of points you can get is 485 points.")
    elif p.choice == "quit":
        confirm = input("Are you sure you want to quit? [y/n]")
        if confirm == 'y':
            print("Thank you for playing. Goodbye.")
            sys.exit()
    elif p.choice == "back":
        if not p.previous_actions:
            print("Sorry, you cannot go back. This is where you started.")
        elif p.previous_actions == [-1]:
            print("Sorry, you cannot go back. "
                  "This is because you took a streetcar to get here. "
                  "To go back, you have to take the streetcar on the other side of the road. "
                  "However, that streetcar back is not arriving anytime soon.")
        else:
            previous_action = p.previous_actions[-1]
            if previous_action == 'E':
                p.choice = 'W'
            elif previous_action == 'W':
                p.choice = 'E'
            elif previous_action == 'S':
                p.choice = 'N'
            else:
                p.choice = 'S'
            move(p, location)
            p.previous_actions.pop()
            p.previous_actions.pop()
    else:
        print("Sorry, that is not a valid choice.")


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(1, 3)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]
    while not p.victory:
        location = w.get_location(p.x, p.y)

        if p.total_moves >= 60:
            print("You've reached the maximum number of moves. You lost the game."
                  "However, feel free to continue exploring the map and reach your destination.")

        if location.visits > 0:
            print(location.short)
        else:
            print(location.long)
            p.score += location.points

        location.visits += 1

        if location.num == 20:
            p.previous_actions = [-1]

        print("What to do? \n")
        print("[menu]")
        for action in location.actions:
            print(action)

        if location.num == 39:
            cur_inventory = [item.name for item in p.inventory]
            if 'LuckyPen' in cur_inventory and 'CheatSheet' in cur_inventory and 'T-Card' in cur_inventory:
                drop_final_items = input("Congratulations, you've reached the Exam Centre. "
                                         "You have everything you need for this exam. "
                                         "Please drop your Lucky Pen, Cheat Sheet and T-Card from your inventory. ")
                p.victory = True

        p.choice = input("\nEnter action: ")

        if p.choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            p.choice = input("\nChoose action: ")

        if p.choice in menu:
            do_action(w, p, location)
        else:
            move(p, location)
        print(p.score)

    if p.total_moves <= 60:
        print("Congratulations! You arrived at the exam on time with everything you need. You won the game!")
        print("Your total score is " + str(p.score) + ", " + str(485 - p.score) +
              " points away from the maximum score you can get")
        print("Thanks for playing the game! Have a nice day!")
    else:
        print("You are sitting on your desk, the examiner comes and looks at your T-Card..."
              "Unfortunately, you spent way too much time finding your lost stuff, and you missed your exam!"
              "The exam you are sitting at is in fact a second year HPS exam... Oh no."
              "Ugh, how unfortunate. Better luck next time!")
