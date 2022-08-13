import pandas as pd
import connect_sql as cs

class DataFromDB:
    cnxn, cursor = cs.sql_connect()

    def select_data(selected_place):
        print('start selecting data from database')

        query = "SELECT * FROM polish_market WHERE place LIKE '" + selected_place + "'"
        df = pd.read_sql(query, DataFromDB.cnxn)

        print('data selected')

        return df

    def import_places(self):
        print('start selecting data from database')

        place_query = 'SELECT DISTINCT place FROM polish_market'
        df = pd.read_sql(place_query, DataFromDB.cnxn)

        print('data selected')

        return df



if __name__ == '__main__':
    df = DataFromDB().import_places()
    print(df.head())
    df2 = DataFromDB.select_data(df.iloc[1,0])
    print(df2.head())

