import pandas as pd
import connect_sql as cs


class DataFromDB:

    @property
    def select_data(selected_place):
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        query = "SELECT * FROM polish_market WHERE "

        if len(selected_place) == 1:
            query = query + "place LIKE '" + selected_place[0] + "'"
            df = pd.read_sql(query, con)
        else:
            list_len = len(selected_place) - 1
            for i, place in enumerate(selected_place):
                if i == list_len:
                    query += "place LIKE '" + selected_place[i] + "'"
                else:
                    query += "place LIKE '" + selected_place[i] + "' OR "
            df = pd.read_sql(query, con)

        print('data selected')
        con.close()
        return df

    def import_places(self):
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        place_query = 'SELECT DISTINCT place FROM polish_market'
        df = pd.read_sql(place_query, con)

        print('data selected')
        con.close()
        return df


if __name__ == '__main__':
    list = ['Polska']
    print(len(list))
    print(DataFromDB.select_data)
