import pandas as pd
import connect_sql as cs


class DataFromDB:

    @staticmethod
    def select_data(selected_place):
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        query = """
            SELECT pm.*, ps.salary_brutto
            FROM polish_market pm
            LEFT JOIN polish_salaries ps
            ON pm.place = ps.place AND pm.date = ps.date
            WHERE pm.place LIKE :selected_place
            """
        params = {'selected_place': selected_place[0]}

        if len(selected_place) > 1:
            query += " OR " + " OR ".join(["pm.place LIKE :p%d" % i for i in range(1, len(selected_place))])
            params.update({"p%d" % i: selected_place[i] for i in range(1, len(selected_place))})



        df = pd.read_sql_query(query, con, params=params)

        print('data selected')
        con.close()
        return df


    @staticmethod
    def import_places():
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        place_query = 'SELECT DISTINCT place FROM polish_market'
        df = pd.read_sql(place_query, con)

        print('data selected')
        con.close()
        return df


if __name__ == '__main__':
    lista = ['POMORSKIE']
    print(len(lista))
    print(DataFromDB.select_data(lista).tail())
