#!/usr/bin/python3
import time
from map import rooms
from player import *
from items import *
from gameparser import *
from itemsimage import *
import getpass
import pickle
import datetime

timer_duration = 1800 # 30 minutes
save_slot = None
time_elapsed_prev_sessions = None

def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string).
    """

    item = ""
    for itemposition, each_item in enumerate(items):
        current_item = each_item["name"]
        if len(items[itemposition::]) > 1:
            item = item + current_item + ", "
            continue
        item += current_item
    return item


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. This function uses list_of_items()
    to produce a comma-separated list of item names.
    """

    if room["items"] != []:
        roomitems = "There is " + list_of_items(room["items"]) + " here.\n"
        print(roomitems)


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.".
    """

    inventory = [item["name"] for item in items]
    inventory_list = ""
    
    if items == []:
        print("Your inventory is empty.")
        print()
    else:
        for i in inventory:
            inventory_list += i + ", "
        inventory_list = inventory_list.rstrip(", ")

        print("You have", inventory_list + ".")
        print()


def print_room(room, timer_string):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. If there are any items in the room, they are to be
    printed using the print_room_items().
    """
    
    # Displays oxygen on the right with changing oxygen
    if len(str(oxygen)) == 3:
        gap_length = 48 - len(room["name"])
    elif len(str(oxygen)) == 2:
        gap_length = 49 - len(room["name"])
    else:
        gap_length = 50 - len(room["name"])

    # Display room name
    print()
    print("="*60)
    print()
    print(room["name"].upper() + gap_length * " " + "Oxygen: " + str(oxygen) + "%")
    print(" "*44+timer_string)
    print()
    # Display room description
    print(room["description"])
    print()

    print_room_items(room)

def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads.
    """

    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:
    """

    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print
    """

    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    print_take_drop_actions(room_items, "take",)
    print_take_drop_actions(inv_items, "drop",)
    print_use_oxygen_actions(inv_items)
    present_items = inv_items + room_items
    print_repair_actions(present_items)
    print_contact_action(inv_items)
    
    print("What do you want to do?")

def print_take_drop_actions(items, action): # takes list of items and string action (drop or take)
    for item in items:
        if item["mobile"]:
            toPrint = action.upper() + " " + item["name"].upper() + " to " + action.lower() + " " + item["name"] + "."
            print(toPrint)

def print_repair_actions(items):
    for item in items:
        if item["broken"]:
            toPrint = "REPAIR" + " " + item["name"].upper() + " to " + "repair" + " " + item["name"] + "."
            print(toPrint)

def print_use_oxygen_actions(items):
    for item in items:
        if item["consumable"]:
            toPrint = "USE" + " " + item["name"].upper() + " to " + "refill oxygen by" + " " + str(item["oxygen"]) + "%."
            print(toPrint)

def print_contact_action(items):
        if current_room == rooms["Control Centre"]:
                toPrint = "CONTACT authorities in NASA."
                print(toPrint)


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" and a players's choice
    "chosen_exit" whether the player has chosen a valid exit. It returns True if
    the exit is valid, and False otherwise. Assume that the name of the exit has
    been normalised by the function normalise_input().
    """

    return chosen_exit in exits

def add_oxygen(amount):
    """Adds amount to player's oxygen level, not increasing it above a maximum level (currently 100)
    """

    global oxygen

    max_oxygen = 100
    oxygen += amount
    if oxygen > max_oxygen:
        oxygen = max_oxygen


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """

    global current_room
    v_exits = current_room["exits"]
    if is_valid_exit(v_exits, direction):  # checking if the exit is valid for the current room.
        if current_room["exits"][direction] == "Storage Cubby":
            print("\nThe storage compartment is locked, requiring a password to open.")
            print("However, a riddle is written on a note attached to the lock:")
            print("\n   I'm the largest in our cosmic crew, a giant sphere of gas, that's true. " + "\n" +
                  "   With bands of clouds of varying hue, my Great Red Spot's a famous view. " + "\n" +
                  "   I've got many moons, a hundred or more, a massive magnetosphere, a cosmic lore." + "\n" +
                  "   In our solar system, I truly soar, a gas giant you can't ignore." + "\n   What am I?")
            user_answer = normalise_input(input("> "))
            if len(user_answer) != 0 and user_answer[0] == "jupiter":
                current_room = move(v_exits,direction)
            else:
                print("INCORRECT ANSWER")
        else:
            current_room = move(v_exits, direction)  # moves you to the next room.
    else:
        print("You cannot go there.")
        #input("[Press enter to continue]")
        getpass.getpass("[Press enter to continue]")

def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """

    if item_id in items:
        item = items[item_id]
        if item in current_room["items"] and item["mobile"]:
            inventory.append(item)
            current_room["items"].remove(item)
        else:
            print("You cannot take that.")
            input("[Press enter to continue]")
    else:
        print("You cannot take that.")
        #input("[Press enter to continue]")
        getpass.getpass("[Press enter to continue]")

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """

    if item_id in items:
        item = items[item_id]
        if item in inventory:
            current_room["items"].append(item)
            inventory.remove(item)
        else:
            print("You cannot drop that.")
            #input("[Press enter to continue]")
            getpass.getpass("[Press enter to continue]")
    else:
        print("You cannot drop that.")
        #input("[Press enter to continue]")
        getpass.getpass("[Press enter to continue]")
        
def execute_repair(item_id):
    """Takes item_id as an argument + attempts to change the "broken" attribute 
    of this item from "True" to "False"
    """

    global objectives
    if item_id in items: # if the item exists
        item = items[item_id]
        if item in inventory or item in current_room["items"]: # if the item is in the inventory or in the current_room
            if item["broken"]:
                can_fix = True
                items_missing = []
                for item_needed_id in item["items to fix"]:
                    item_needed = items[item_needed_id]
                    if not(item_needed in inventory):
                        can_fix = False
                        items_missing.append(item_needed["name"])
                if can_fix:
                    item["broken"] = False
                    print("You successfully fixed the " + item["name"])
                    objectives += 1
                    getpass.getpass("[Press enter to continue]")
                else:
                    if len(items_missing) > 1:
                        items_missing.insert(-1," and")
                    to_print = "You need "
                    for i, missing_item in enumerate(items_missing):
                        to_print += missing_item
                        if i < len(items_missing) - 3:
                            to_print += ", "
                        elif i == len(items_missing) - 2:
                            to_print += " "
                    to_print += " to repair this."
                    print(to_print)
                    getpass.getpass("[Press enter to continue]")
            else:
                print("This item isn't broken")
                getpass.getpass("[Press enter to continue]")
        else:
            print("You don't have this item.")
            getpass.getpass("[Press enter to continue]")
    else:
        print("You can't repair this.")
        #input("[Press enter to continue]")
        getpass.getpass("[Press enter to continue]")

def execute_use(item_id):
    """Takes item_id as an argument and attempts to use the item, consuming it
    and increasing oxygen"""

    if item_id in items:
        item = items[item_id]
        if item in inventory:
            if item["consumable"]:
                # add to oxygen and remove item from inventory
                add_oxygen(items[item_id]["oxygen"])
                inventory.remove(item)
            else:
                print("This item isn't edible.")
                getpass.getpass("[Press enter to continue]")
        else:
            print("You don't have this item.")
            getpass.getpass("[Press enter to continue]")
    else:
        print("You can't eat this.")
        getpass.getpass("[Press enter to continue]")

def execute_contact(item_id):
    """Takes item_id as an argument and attempts to contact the authorities.
    """
    global objectives
    if (items["power supply"]["broken"] == False):
        if items["password"] in inventory:
            if items["escape pod"]["broken"] == False:
                print("CONGRATULATIONS! You have contacted NASA successfully. They are awaiting your arrival.")
                print("Now return to the escape pod to leave the space station.")
                objectives += 1
                getpass.getpass("[Press enter to continue]")
            else:
                print("You need to repair the escape pod before you can tell NASA to await your arrival.")
                getpass.getpass("[Press enter to continue]")
        else:
            print("You need the computer's password to contact the authorities.")
            getpass.getpass("[Press enter to continue]")
    else:
        print("You need to repair the power supply before you can turn on the computer.")
        getpass.getpass("[Press enter to continue]")

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.
    """
    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            item = " ".join(command[1:]) # Allow items with multiple strings (wire cutter) to be picked up
            execute_take(item)
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            item = " ".join(command[1:]) # Allow items with multiple strings (wire cutter) to be dropped
            execute_drop(item)
        else:
            print("Drop what?")

    elif command[0] == "use":
        if len(command) > 1:
            item = " ".join(command[1:]) # Allow items with multiple strings (small oxygen tank) to be used
            execute_use(item)
        else:
            print("Drop what?")
            
    elif command[0] == "repair" or command[0] == "fix":
        if len(command) > 1:
            item = " ".join(command[1:]) # Allow items with multiple strings (power supply) to be repaired
            execute_repair(item)
        else:
            print("Repair what?")

    elif command[0] == "contact":
        execute_contact(command[0])

    elif command[0] != "exit":
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.
    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:
    """

    # Next room to go to
    return rooms[exits[direction]]


def update_oxygen(oxygen_loss_time):

    global oxygen

    # Rate of oxygen loss
    o2_loss_rate = 6.5

    current_time = time.time()
    elapsed_time = current_time - oxygen_loss_time

    # Calculates how much oxygen to take away
    cycles = int(elapsed_time / o2_loss_rate)

    if elapsed_time >= o2_loss_rate:
        oxygen -= cycles
        oxygen = max(oxygen, 0)
        oxygen_loss_time = current_time
    
    return oxygen_loss_time

def winner_text():
    print("┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼")
    print("┼┼┼▀███┼┼██▀┼███▀▀▀███┼▀███┼┼┼┼██▀┼┼┼")
    print("┼┼┼┼┼██┼┼██┼┼██┼┼┼┼┼██┼┼┼██┼┼┼┼██┼┼┼┼")
    print("┼┼┼┼┼┼┼██┼┼┼┼██┼┼┼┼┼██┼┼┼██┼┼┼┼██┼┼┼┼")
    print("┼┼┼┼┼┼┼██┼┼┼┼██┼┼┼┼┼██┼┼┼██┼┼┼┼██┼┼┼┼")
    print("┼┼┼┼┼┼┼██┼┼┼┼███▄▄▄███┼┼┼████████┼┼┼┼")
    print("┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼")
    print("┼██┼┼┼┼┼┼┼██┼┼████████┼┼┼┼████████┼┼┼")
    print("┼██┼┼┼┼┼┼┼██┼┼┼┼┼██┼┼┼┼┼┼┼██┼┼┼┼██┼┼┼")
    print("┼██┼┼┼┼┼┼┼██┼┼┼┼┼██┼┼┼┼┼┼┼██┼┼┼┼██┼┼┼")
    print("┼██┼┼┼▄┼┼┼██┼┼┼┼┼██┼┼┼┼┼┼┼██┼┼┼┼██┼┼┼")
    print("┼██┼┼┼█┼┼┼██┼┼┼┼┼██┼┼┼┼┼┼┼██┼┼┼┼██┼┼┼")
    print("┼███▄█▀█▄███┼┼████████┼┼▄███┼┼┼┼███▄┼")
    print("┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼")
    print()
    time.sleep(2)

def game_over_text():
    print("┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼")
    print("┼███▀▀▀██┼███▀▀▀███┼███▀█▄█▀███┼██▀▀▀┼")
    print("┼██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼█┼┼┼██┼██┼┼┼┼")
    print("┼██┼┼┼▄▄▄┼██▄▄▄▄▄██┼██┼┼┼▀┼┼┼██┼██▀▀▀┼")
    print("┼██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██┼┼┼┼")
    print("┼███▄▄▄██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██▄▄▄┼")
    print("┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼")
    time.sleep(1)
    print("┼███▀▀▀███┼▀███┼┼██▀┼██▀▀▀┼██▀▀▀▀██▄┼┼")
    print("┼██┼┼┼┼┼██┼┼┼██┼┼██┼┼██┼┼┼┼██┼┼┼┼┼██┼┼")
    print("┼██┼┼┼┼┼██┼┼┼██┼┼██┼┼██▀▀▀┼██▄▄▄▄▄▀▀┼┼")
    print("┼██┼┼┼┼┼██┼┼┼██┼┼█▀┼┼██┼┼┼┼██┼┼┼┼┼██┼┼")
    print("┼███▄▄▄███┼┼┼─▀█▀┼┼─┼██▄▄▄┼██┼┼┼┼┼██▄┼")
    print("┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼")
    print()
    time.sleep(2)


def loading_text(seconds, wait_time=0.7):
    print("Loading", end="")
    for i in range(int(seconds / wait_time)):
        print(".", end="", flush=True)
        time.sleep(wait_time)

def summary_objectives():
    print("""
SUMMARY:
You are on board of space station.
Your colleagues are dead because of an accident that occurred in the laboratory.
Your job now is to repair the space station and contact the authorities for help.""")
    print()
    print("OBJECTIVES:" + "\n" + "1. Repair the power supply." + "\n" + "2. Repair the escape pod." + "\n" + "3. Contact Nasa.")

def load_from_dict(dictionary):
    """This function loads from a dictionary all values that may change over the course of the game"""
    global inventory, current_room, oxygen, objectives, time_elapsed_prev_sessions
    inventory = dictionary["inventory"]
    current_room = rooms[dictionary["current room id"]]
    oxygen = dictionary["oxygen"]
    objectives = dictionary["objectives"]
    for room_id in rooms:
        items_list = []
        for item_id in dictionary["room item ids"][room_id]:
            items_list.append(items[item_id])
        rooms[room_id]["items"] = items_list
    for item_id in dictionary["broken items status"]:
        items[item_id]["broken"] = dictionary["broken items status"][item_id]
    time_elapsed_prev_sessions = dictionary["time elapsed prev sessions"]

def create_save_dict(elapsed_time):
    """This function saves the current state of changeable values in the game 
    as a dictionary, to allow saving in a single save file"""
    save_dict = {}
    save_dict["inventory"] = inventory
    save_dict["current room id"] = current_room["id"]
    save_dict["oxygen"] = oxygen
    save_dict["objectives"] = objectives
    save_dict["room item ids"] = {}
    for room_id in rooms:
        items = []
        for item in rooms[room_id]["items"]:
            items.append(item["id"])
        save_dict["room item ids"][room_id] = items
    save_dict["broken items status"] = {"power supply":item_powersupply["broken"],
                                        "escape pod":item_escapepod["broken"],
                                        }
    save_dict["time elapsed prev sessions"] = elapsed_time
    save_dict["timestamp"] = datetime.datetime.now()
    return save_dict

def read_savefile():
    try:
        with open("save_file.txt","rb") as save_file:
            savefile_list = pickle.load(save_file)
        return savefile_list
    except FileNotFoundError:
        return []

def write_savefile(to_write):
    with open("save_file.txt","wb") as save_file:
        pickle.dump(to_write,save_file)

def save_game(current_save):
    saves_list = read_savefile()
    if save_slot > len(saves_list) - 1: # if save slot out of range, i.e. a new game
        saves_list.append(current_save)
    elif current_save == None:
        saves_list.pop(save_slot)
    else:
        saves_list[save_slot] = current_save
    
    write_savefile(saves_list)

def display_save_slots(saves_list):
    last_played = ["[Empty]","[Empty]","[Empty]"]
    time_remaining = ["","",""]
    for save_slot_number in range(0,len(saves_list)):
        last_played[save_slot_number] = ("Last played: " + str(saves_list[save_slot_number]["timestamp"])[:16])
        time_remaining[save_slot_number] = (1800-saves_list[save_slot_number]["time elapsed prev sessions"])
    gap = 25
    print()
    print("SLOT 1" + " "*gap + "SLOT 2" + " "*gap + "SLOT 3")
    print(last_played[0] +" "*(31-len(last_played[0])) + last_played[1] +" "*(31-len(last_played[1])) + last_played[2])

def new_game():
    load_from_dict(start_values)
    summary_objectives()
    getpass.getpass("[Press enter to view the map]")
    map()
    summary_objectives()
    getpass.getpass("[Press enter to start the game]")
    gameloop()

def load_game():
    load_from_dict(read_savefile()[save_slot])
    gameloop()

def main_menu():
    while True:
        global save_slot
        game_title()
        print("NEW GAME")
        print("LOAD GAME")
        print("EXIT")
        
        command = normalise_input(input("> "))
        if len(command) != 0:
            if len(command) > 1:
                if command[0] == "new" and command[1] == "game":
                    saves_list = read_savefile()
                    if len(saves_list) < 3: # If there is an empty save slot
                        save_slot = len(saves_list) # Set save slot to lowest empty one
                        new_game()
                    else:
                        print("\nYou have no empty save slots. Select a save to overwrite or type CANCEL to return to main menu.")
                        display_save_slots(saves_list) # allow to choose which to overwrite
                        command = normalise_input(input("\n> "))
                        if len(command) != 0:
                            if command[-1] in ["1","2","3"]:
                                save_slot = int(command[-1]) - 1
                                new_game()
                elif command[0] == "load" and command[1] == "game":
                    saves_list = read_savefile()
                    display_save_slots(saves_list)
                    command = normalise_input(input("\n> "))
                    if len(command) != 0:
                        if command[-1] in ["1","2","3"]:
                            if int(command[-1])-1 < len(saves_list):
                                save_slot = int(command[-1]) - 1
                                load_game()
                            else:
                                print("This save slot is empty.")
            elif command[0] == "exit":
                break

def gameloop():
    session_start_time = time.time()
    oxygen_loss_time = session_start_time
    command = [None]
    while len(command) == 0 or command[0] != "exit" :
        
        elapsed_time = time.time() - session_start_time + time_elapsed_prev_sessions
        if elapsed_time >= timer_duration:
            game_over_text()
            print("TIME'S UP! YOU WERE UNSUCCESSFUL IN COMPLETING THE GAME, BETTER LUCK NEXT TIME.")
            getpass.getpass("[Press enter to continue]")
            save_game(None)
            break
        
        oxygen_loss_time = update_oxygen(oxygen_loss_time)
        if oxygen <= 0:
            game_over_text()
            print("YOU HAVE DIED!!")
            getpass.getpass("[Press enter to continue]")
            save_game(None)
            break

        # remaining time
        remaining_time = timer_duration - elapsed_time
        mins, secs = divmod(remaining_time,60)
        mins = int(mins)
        secs = int(secs)
        timer_string = f"Time left: {mins:02d}:{secs:02d}"
        # the f here is for the formatting, and the d stands for integers.
        
        print_room(current_room,timer_string)
        print_inventory_items(inventory)
        
        command = menu(current_room["exits"], current_room["items"], inventory)
        execute_command(command)
        
        save_game(create_save_dict(elapsed_time))
        
        if objectives > 2 and current_room["id"] == "Escape Pod":
            winner_text()
            print("CONGRATULATIONS! You have successfully completed the objectives and have won the game.")
            save_game(None)
            break

# This is the entry point of our program
def main():

    global oxygen
    global objectives
    main_menu()


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
