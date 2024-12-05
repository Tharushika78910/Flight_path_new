import mysql.connector

from connector import connect_to_db

"""#Function for getting airport codes
def get_airport_codes():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        query = f"SELECT airport_code FROM new_airports"
        cursor.execute(query)

        airports = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return airports

    except mysql.connector.Error as err:
        print(f"Error getting airport codes: {err}")
        return None"""



"""#Create a new player
def create_player():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
    
        insert_query = f"INSERT INTO player (player_id, screen_name, start_location, end_location, destination, total_money, cargo_collected ) VALUES (%s, %s, 'LEMD', %s, 'LIPE', 0, 0)"
        cursor.execute(insert_query)
        conn.commit()
    
        cursor.execute("Select LAST_INSERT_ID()")
        game_id = cursor.fetchone()[0]
        return game_id
    
    except mysql.connector.Error as err:
        print(f"Error creating a player: {err}")
        return None

#function to retrieve a player's current state
def get_current_status():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        get_query = f"SELECT * FROM player WHERE player_id = %s"
        cursor.execute(get_query)
        conn.commit()

        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print(f"Error getting current status: {err}")
        return None"""


#function to get a goal for an airport
def get_goal():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        get_query = f"SELECT a.airport_code, g.type AS goal_type FROM new_airports a JOIN goal g ON a.goal_type = g.goal_id;"
        cursor.execute(get_query)
        conn.commit()

        result_goal = cursor.fetchall()
        return result_goal

    except mysql.connector.Error as err:
        print(f"Error getting airport goal: {err}")
        return None

#function to collect cargoes.
def collect_cargo():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        collect_query = f"UPDATE player SET cargo_collected = cargo_collected + 1 WHERE player_id = %s;"
        cursor.execute(collect_query)
        conn.commit()

        result_cargo = cursor.fetchall()
        return result_cargo

    except mysql.connector.Error as err:
        print(f"Error collecting cargo: {err}")
        return None

#function to collect money from cargoes
def cargo_money():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        money_query = f"UPDATE player SET player.total_money = goal.value WHERE player_id = %s;"