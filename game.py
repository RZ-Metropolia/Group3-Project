# The main game program

import gamefunctions
import dbinteract

try:
    # Display the title and get the player_name and player_id for current game
    player_name = gamefunctions.get_player_name()
    player_id = dbinteract.get_player_id(player_name)

    # Ask the players if they want to read the game introduction or not
    gamefunctions.read_intro()

    # Initialize the stock of the goods in different airport
    dbinteract.initialize_goods_in_different_airports()

    # Before the game starts, do the following condition checks
        # Get time_left of the player from the database, if time_left <= 0 => Game Over!
    dbinteract.check_time_left(player_id)
        # Get current_funds of the player from the database, if current_funds >= 1,000,000 => Thank you for playing
    dbinteract.check_funds(player_id)

    # Get the information of the player from database and display it.
    dbinteract.display_player_info(player_id)

    # Command List
    gamefunctions.command_list(player_id)
except KeyboardInterrupt:
    print("\nQuit")