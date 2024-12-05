import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='12345',
            database='flight_path',
            autocommit=True

        )
        if conn.is_connected():
            print("Connection Established")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
