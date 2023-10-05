import pandas as pd
import connect_sql as cs

from download_from_csv import download_from_csv

class download_from_csv_values:

    @staticmethod
    def add_csv(link_csv):
        # upload csv file, drop unnesesery columns and NaN rows
        df = pd.read_csv(link_csv, sep=";")
        df.drop(['Atrybut', 'Unnamed: 9'], axis=1, inplace=True)
        df.dropna(inplace=True)

        # change column names and add column with date
        df.columns = ['code', 'place', 'quater', 'transactions', 'area', 'year', 'value', 'unit']
        df['date'] = df['quater'].apply(download_from_csv.change_quater)
        df['year'] = df['year'].apply(str)
        df['date'] = df['year'].astype(str).str.cat(df['date'])
        df = download_from_csv.create_code(df)
        df.drop(['place', 'quater', 'transactions', 'area', 'year', 'date'], axis=1, inplace=True)

        return df

    @staticmethod
    def upload_data(con, cursor, df, table_name, file_name):
        print(f"starting with file {file_name}")
        print('starting upload to database')
        i = 0;
        for index, row in df.iterrows():
            if i % 10000 == 0:
                print(f"rows imported: {i}")
            cursor.execute(f"INSERT INTO {table_name} (code, value, unit) values(?,?,?)",
                           (row.code, row.value, str(row.unit)))
            i = i+1
        con.commit()
        print('upload success')
        con.close()
        print('connection closed')
    

if __name__ == '__main__':
    print('starting csv upload')
    df_polish_market = download_from_csv_values.add_csv('csv_files/mediana_cen_mieszkan.csv')
    con, cursor = cs.sql_connect()
    download_from_csv_values.upload_data(con, cursor, df_polish_market, "polish_market_count")

    print(df_polish_market.head())