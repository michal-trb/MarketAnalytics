import pyodbc, sqlite3

sessions = {}

def sql_connect():
    print('starting connection with database')
    sql_connection = "DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE=Market.db;Trusted_connection=yes"

    con = sqlite3.connect('Market.db', timeout=100)
    cursor = con.cursor()
    print('connection success')
    return con, cursor

sql_connect()
