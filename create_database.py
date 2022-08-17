import sqlite3

connection = sqlite3.connect('Market.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS polish_market
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, place TEXT, quater TEXT, transactions TEXT, area TEXT, year INT, m2_value NUMBER, unit TEXT, date TEXT )''')
