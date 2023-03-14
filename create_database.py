import sqlite3

def create_database():
    connection = sqlite3.connect('Market.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS polish_market
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, place TEXT, quater TEXT, transactions TEXT, area TEXT, year INT, m2_value INT, unit TEXT, date TEXT )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS polish_salaries
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, place TEXT, quater TEXT, transactions TEXT, year INT, salary_brutto INT, currency TEXT, date TEXT)''')
