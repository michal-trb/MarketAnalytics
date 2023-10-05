import sqlite3

def create_database():
    connection = sqlite3.connect('Market.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS polish_salaries
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, place TEXT, quater TEXT, year INT, salary_brutto INT, currency TEXT, date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS dim_polish_market
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, salary_code INT, place TEXT, quater TEXT, transactions TEXT, area TEXT, year INT, date TEXT )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS fact_polish_market_median_m2
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, value INT, unit TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS fact_polish_market_sum_value
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, value INT, unit TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS fact_polish_market_count
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, value INT, unit TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS fact_polish_market_count_m2
              (id INTEGER PRIMARY KEY  AUTOINCREMENT, code INT, value INT, unit TEXT)''')
    