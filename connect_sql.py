import pyodbc

def sql_connect():
    print('starting connection with database')
    sql_connection = '''DRIVER={SQL Server};
                        SERVER=DESKTOP-S9BTPQ5\MICHALTEST;
                        DATABASE=AnalitykaMieszkan;
                        Trusted_Connection=yes'''
    cnxn = pyodbc.connect(sql_connection)
    cursor = cnxn.cursor()
    print('connection success')
    return cnxn, cursor

