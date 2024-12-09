import random

import mysql.connector
from mysql.connector import cursor

from connector import connect_to_db
from queries import start_game
from queries import fly_to_airport
from queries import buy_fuel
from queries import collect_cargo
from queries import check_status

# Main game loop
start_game()
cursor.execute("SELECT LAST_INSERT_ID()")
player_id = cursor.fetchone()

while True:
    print("\nOptions:")
    print("1 - Fly to next airport")
    print("2 - Buy fuel")
    print("3 - Collect cargo")
    print("4 - Check status")
    print("5 - Exit game")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        target_airport = input("Enter the airport code: ")
        fly_to_airport(player_id, target_airport)
    elif choice == 2:
        fuel_amount = int(input("Enter the amount of fuel to buy: "))
        buy_fuel(player_id, fuel_amount)
    elif choice == 3:
        collect_cargo(player_id)
    elif choice == 4:
        check_status(player_id)
    elif choice == 5:
        print("Exiting game. Thank you for playing!")
        break
    else:
        print("Invalid choice. Please try again.")