import pandas as pd
import connect_sql as cs

class DataFromDB:
    cnxn, cursor = cs.sql_connect()

    def select_data(selected_place):
        print('start selecting data from database')

        query = "SELECT * FROM polish_market WHERE "

        if len(selected_place) == 1:
            query = query + "place LIKE '" + selected_place[0] + "'"
            df = pd.read_sql(query, DataFromDB.cnxn)
        else:
            list_len = len(selected_place) - 1
            for i, place in enumerate(selected_place):
                if i == list_len:
                    query = query + "place LIKE '" + selected_place[i] + "'"
                else:
                    query = query + "place LIKE '" + selected_place[i] + "' OR "
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
    list = ['Polska']
    print(len(list))
    print(DataFromDB.select_data(list))

