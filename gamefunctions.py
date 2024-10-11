# Game functions without direct connection with database

import time
import geopy.distance
import dbinteract

def command_list(player_id):
    """Display command list and interact with player

    """
    prompt =  """
Commands:
1. Visit local store
2. Move to another location
3. Check inventory
4. Quit the game
+--------------------------------------------+
"""
    print(prompt)

    user_input = input("Please make your choice:")

    while user_input not in ["1", "2", "3", "4"]:
        user_input = input("Invalid input, please try again:")
    if user_input == "1":
        store_menu(player_id)
    elif user_input == "2":
        travel_menu(player_id)
    elif user_input == "3":
        dbinteract.check_inventory(player_id)
    elif user_input == "4":
        exit()

def get_player_name():
    """Display the title and return the player_name before game starts

    """
    title = """
*********************************************************************  
 __  _  _ ____ ____ _ ____ ____ _  _    ___ _   _ ____ ____ ____ _  _ 
|__| |\/| |___ |__/ | |    |__| |\ |     |   \_/  |    |  | |  | |\ | 
|  | |  | |___ |  \ | |___ |  | | \|     |    |   |___ |__| |__| | \|

*********************************************************************

                        1. New Game
                        2. Continue
                        3. Quit
"""
    print(title)

    user_input = input("Enter your choice: ")   

    while user_input not in ["1", "2", "3"]:
        print("Invalid input. Please try again.")
        user_input = input("Enter your choice: ")

    if user_input == "1":
        player_name = input("Please enter your name: ")
        while player_name.title() in dbinteract.get_existing_names():
            player_name = input("Name already exists. Please enter a new name: ")
        dbinteract.register_new_player(player_name.title())

        print(f"Welcome to American Tycoon! {player_name.title()}!")

        return player_name.title()

    elif user_input == "2":
        if not dbinteract.get_existing_names():
            print("\nNo unfinished game found. Please start a new game.")
            exit()
        else:
            player_name = get_saved_name()
            print(f"Welcome back! {player_name.title()}!")

            return player_name.title()

    elif user_input == "3":
        exit()

def get_saved_name():
    """Return the saved players' names in game table
    
    """
    print("-----------------------------")
    print("Unfinished games: ")
    for index, name in enumerate(dbinteract.get_existing_names()):
        print(f"{index + 1}. {name}")
    print("-----------------------------")
    player_name = input("Please enter your name: ")
    while player_name.title() not in dbinteract.get_existing_names():
        player_name = input("Invalid names. Please try again: ")

    return player_name.title()

def read_intro():
    """Ask the player if they want to read the introduction or not
    
    """
    prompt = f"Do you want to read the introduction?(y/n)"
    user_input = input(prompt)
    while user_input.lower() not in ["y", "n"]:
        print("Invalid input. Please try again.")
        user_input = input(prompt)

    if user_input.lower() == "n":
        return None
    else:
        introduction = """
------------------------------------------------------------------------------------------------------------------------
You are an ambitious green hand who is ready to become the richest tycoon in the U.S.
The first step of your commercial legend is to make more than 1,000,000 dollars during the next 15 days(360 hours).
In the beginning of your journey, you will start at a random place with 10,000 dollars as your initial capital.
After that, you can freely buy or sell goods from local stores before the deadline.
You can also choose to move up to 15 different places in the U.S.
Be aware that travelling takes time which depends on the distance between your current location and the destination.
Good luck!
------------------------------------------------------------------------------------------------------------------------
"""
        print(introduction)
        time.sleep(2)
        user_input = input("Press Enter to continue...")

def store_menu(player_id):
    """Display the store menu and interact with the player

    """
    store_commands = '''
+++++++++++++++++++++++++++++++++++++++++++++++++++++
1. Buy 
2. Sell 
3. Back
+++++++++++++++++++++++++++++++++++++++++++++++++++++ 
'''
    print(store_commands)

    user_input = input("Please make your choice:")
    while user_input not in ["1", "2", "3"]:
        user_input = input("Invalid input, please try again:")

    if user_input == "1":
        dbinteract.buy_goods(player_id)
        time.sleep(1)
        store_menu(player_id)
    elif user_input == "2":
        dbinteract.sell_goods(player_id)
        dbinteract.check_funds(player_id)
        time.sleep(1)
        store_menu(player_id)
    elif user_input == "3":
        dbinteract.display_player_info(player_id)
        command_list(player_id)

def travel_menu(player_id):
    """Display the travel menu and interact with the player

    """
    travel_commands = '''
+++++++++++++++++++++++++++++++++++++++++++++++++++++
1. Travel
2. Back
+++++++++++++++++++++++++++++++++++++++++++++++++++++ 
'''
    print(travel_commands)

    user_input = input("Please make your choice:")
    while user_input not in ["1", "2"]:
        user_input = input("Invalid input, please try again:")

    if user_input == "1":
        current_airport_ident = dbinteract.get_current_location(player_id)

        list_airports(current_airport_ident)

        destination_ident = get_destination(player_id)
        distance = get_distance(current_airport_ident, destination_ident)
        travel_time = get_travel_time(distance)

        travel_double_check(current_airport_ident, destination_ident, travel_time, player_id)

    elif user_input == "2":
        dbinteract.display_player_info(player_id)
        command_list(player_id)

def list_airports(current_airport_ident):
    """Display the airports list

    """
    airport_idents = dbinteract.get_airports_idents()
    airport_names = dbinteract.get_airports_names()

    print("\nAirports list")
    print("-" * 80)
    print("{:<10} {:<45} {:<15}".format("Ident", "Name", "Travel Time"))
    for index, airport_ident in enumerate(airport_idents):
        distance = get_distance(current_airport_ident, airport_ident)
        travel_time = get_travel_time(distance)

        print("{:<10} {:<45} {:<15}".format(airport_ident, airport_names[index], travel_time))
    print("-" * 80)

def get_destination(player_id):
    """Get the travel destination from the input of the player

    """
    airport_idents = dbinteract.get_airports_idents()

    user_input = input("Please enter the destination ident code:")
    while user_input.upper() not in airport_idents:
        user_input = input("Invalid value. Please input again: ")

    return user_input.upper()

def get_distance(ident1, ident2):
    """Return the distance between two airports

    """
    coordinate1 = dbinteract.get_coordinate(ident1)
    coordinate2 = dbinteract.get_coordinate(ident2)

    return geopy.distance.distance(coordinate1, coordinate2).km

def get_travel_time(distance):
    """Return the travel time of certain distance

    """
    travel_time = distance / 500

    return float(f"{travel_time:.1f}")

def travel_double_check(current_ident, destination_ident, travel_time, player_id):
    """Double check if the player want to make the travel, and process accordingly

    """
    current_location_name = dbinteract.get_airport_name(current_ident)
    destination_location_name = dbinteract.get_airport_name(destination_ident)
    time_left = dbinteract.get_player_time_left(player_id)

    print(f"You are going to travel from ({current_ident}:{current_location_name}) to ({destination_ident}:{destination_location_name}).")
    print(f"It will take {travel_time} hours, and now you have {time_left} hours left.")

    user_input = input("Are you sure about this travel?(y/n)")
    while user_input.lower() not in ["y", "n"]:
        user_input = input("Invalid input, please try again:")
    if user_input == "y":
        print("Flying...")
        time.sleep(1)
        print("Flying..")
        time.sleep(1)
        print("Flying.")
        time.sleep(1)

        dbinteract.update_player_current_location(player_id, destination_ident)
        dbinteract.update_player_time_left(player_id, travel_time)
        dbinteract.check_time_left(player_id)
        dbinteract.display_player_info(player_id)
        command_list(player_id)
    elif user_input == "n":
        travel_menu(player_id)