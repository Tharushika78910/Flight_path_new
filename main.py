from random import random

import mysql.connector
from connector import connect_to_db
import queries
from queries import get_airport_codes

airports = get_airport_codes()


high_consumption_airport = random.choice(airports, 3)