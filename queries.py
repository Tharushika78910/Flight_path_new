import mysql.connector
from math import radians, sin, cos, sqrt, atan2
from connector import connect_to_db


def start_game():
    conn = connect_to_db()
    cursor = conn.cursor()

    player_name = input("Enter your name: ")
    print(f"Welcome, {player_name}!")
    cursor.execute("INSERT INTO player (screen_name, fuel_amount, total_money, cargo_collected, start_location, destination, end_location) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (player_name, 1000, 0, 0, 'LEMD', 'LIPE', 'LEMD'))
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    player_id = cursor.fetchone()
    player_id = int(player_id)
    print(f"Player created with ID: {player_id}")
    cursor.close()
    conn.close()



# Function to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# Function to fly to the next airport
def fly_to_airport(player_id, target_airport):
    # Debugging
    print(f"Debug: player_id = {player_id}, type = {type(player_id)}")

    # Validate and convert player_id
    try:
        player_id = int(player_id)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Invalid player_id: {player_id}. Must be an integer. Error: {e}")

    # Validate target_airport
    if not isinstance(target_airport, str):
        raise TypeError("target_airport must be a string")

    # Database operations
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT latitude_deg, longitude_deg FROM new_airports WHERE airport_code = %s", (target_airport,))
    target_coords = cursor.fetchone()
    cursor.execute(
        "SELECT latitude_deg, longitude_deg FROM new_airports WHERE airport_code = (SELECT end_location FROM player WHERE player_id = 22)",
        (player_id,)
    )
    current_coords = cursor.fetchone()


    if target_coords and current_coords:
        distance = calculate_distance(current_coords[0], current_coords[1], target_coords[0], target_coords[1])
        fuel_needed = int(2 * distance)  # 2 fuel units per km

        cursor.execute("SELECT fuel_amount, total_money FROM player WHERE player_id = %s", (player_id,))
        player_stats = cursor.fetchone()

        if player_stats[0] < fuel_needed:
            print("Not enough fuel. Buy fuel or choose another airport.")
        else:
            cursor.execute("UPDATE player SET fuel_amount = fuel_amount - %s, end_location = %s WHERE player_id = %s",(fuel_needed, target_airport, player_id))
            conn.commit()
            print(f"Traveled to {target_airport}. Fuel left: {player_stats[0] - fuel_needed}.")
    else:
        print("Invalid airport code.")

# Function to buy fuel
def buy_fuel(player_id, fuel_amount):
    conn = connect_to_db()
    cursor = conn.cursor()

    cost = fuel_amount * 10  # 10 money units per 1 fuel unit
    cursor.execute("SELECT total_money FROM player WHERE player_id = %s", (player_id,))
    money = cursor.fetchone()[0]

    if money >= cost:
        cursor.execute("UPDATE player SET total_money = total_money - %s, fuel_amount = fuel_amount + %s WHERE player_id = %s",
                       (cost, fuel_amount, player_id))
        conn.commit()
        print(f"Bought {fuel_amount} fuel units for {cost} money.")
    else:
        print("Not enough money to buy fuel.")

# Function to collect cargo
def collect_cargo(player_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT end_location FROM player WHERE player_id = %s", (player_id,))
    current_location = cursor.fetchone()[0]
    cursor.execute("SELECT value FROM goal WHERE airport_code = %s", (current_location,))
    result = cursor.fetchone()

    if result:
        cargo_value = result[0]
        cursor.execute(
            "UPDATE player SET total_money = total_money + %s, cargo_collected = cargo_collected + 1 WHERE player_id = %s",
            (cargo_value, player_id))
        conn.commit()
        print(f"Collected cargo worth {cargo_value} money.")
    else:
        print("No cargo available at this airport.")

    cursor.close()
    conn.close()

# Function to check player status
def check_status(player_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player WHERE player_id = %s", (player_id,))
    status = cursor.fetchone()
    print("Player Status:")
    print(f"Name: {status[1]}")
    print(f"Fuel: {status[2]}")
    print(f"Money: {status[3]}")
    print(f"Cargo Collected: {status[4]}")
    print(f"Current Location: {status[5]}")