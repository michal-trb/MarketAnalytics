import pandas as pd
import connect_sql as cs


class DataFromDB:

    @staticmethod
    def select_data(selected_places, selected_areas, selected_transactions, table_name):
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        query = f"""
            SELECT 
                pm.code,
                pm.place,
                pm.transactions,
                pm.area,
                pm.year,
                pm.date,
                val.value
            FROM dim_polish_market pm
            LEFT JOIN {table_name} val
            ON pm.code = val.code
            WHERE 
            pm.place LIKE :selected_place
            """

        params = {'selected_place': selected_places[0]}

        if len(selected_places) > 1:
            query += " OR " + " OR ".join(["pm.place LIKE :p%d" % i for i in range(1, len(selected_places))])
            params.update({"p%d" % i: selected_places[i] for i in range(1, len(selected_places))})

        df = pd.read_sql_query(query, con, params=params)
        df = df.query('area == @selected_areas')
        df = df.query('transactions == @selected_transactions')

        print('data selected')
        con.close()
        return df

    @staticmethod
    def select_data_with_salary(selected_places, selected_areas, selected_transactions, table_name):
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        query = f"""
            SELECT DISTINCT
                ps.code,
                pm.place,
                pm.transactions,
                pm.area,
                pm.year,
                pm.date,
                val.value,
                ps.salary_brutto
            FROM dim_polish_market pm
            LEFT JOIN {table_name} val
            ON pm.code = val.code
            LEFT JOIN polish_salaries ps
            on ps.code = pm.salary_code
            WHERE 
            pm.place LIKE :selected_place
            """

        params = {'selected_place': selected_places[0]}

        if len(selected_places) > 1:
            query += " OR " + " OR ".join(["pm.place LIKE :p%d" % i for i in range(1, len(selected_places))])
            params.update({"p%d" % i: selected_places[i] for i in range(1, len(selected_places))})

        df = pd.read_sql_query(query, con, params=params)
        df = df.query('area == @selected_areas')
        df = df.query('transactions == @selected_transactions')

        print('data selected')
        con.close()
        return df

    @staticmethod
    def import_places():
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        place_query = 'SELECT DISTINCT place FROM dim_polish_market'
        df = pd.read_sql(place_query, con)

        print('data selected')
        con.close()
        return df

    @staticmethod
    def import_areas():
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        place_query = 'SELECT DISTINCT area FROM dim_polish_market'
        df = pd.read_sql(place_query, con)

        print('data selected')
        con.close()
        return df
    
    @staticmethod
    def import_transactions():
        print('start selecting data from database')
        con, cursor = cs.sql_connect()

        place_query = 'SELECT DISTINCT transactions FROM dim_polish_market'
        df = pd.read_sql(place_query, con)

        print('data selected')
        con.close()
        return df

if __name__ == '__main__':
    lista = ['POMORSKIE']
    tran = ['ogółem']
    area = ['ogółem']
    print(len(lista))
    print(DataFromDB.select_data_m2(lista, tran, area).tail())

