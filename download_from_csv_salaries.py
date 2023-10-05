import pandas as pd
import connect_sql as cs
import unicodedata
from download_from_csv import download_from_csv

class download_from_csv_salaries:
    
    @staticmethod
    def add_csv(link_csv):
        # upload csv file, drop unnesesery columns and NaN rows
        df = pd.read_csv(link_csv, sep=";", engine='python')
        df.drop(['Wynagrodzenie brutto','Atrybut', 'Unnamed: 8'], axis=1, inplace=True)
        df.dropna(inplace=True)

        # change column names and add column with date
        df.columns = ['code', 'place', 'quater', 'year', 'salary_brutto', 'currency']
        df['date'] = df['quater'].apply(download_from_csv.change_quater)
        df['year'] = df['year'].apply(str)
        df['date'] = df['year'].str.cat(df['date'])
        df['code'] = df['place'].str.replace('\s+', '').str.upper().str.replace('-', '') + df['date'].str.replace('-', '')
        df['code'] = df['code'].apply(download_from_csv.remove_polish_chars)
        df['date'] = pd.to_datetime(df['date'])
        df['salary_brutto'] = df['salary_brutto'].replace(',','.', regex=True)
        df.sort_values('date', inplace=True)
        return df

    @staticmethod
    def upload_data(con, cursor, df, file_name):
        print(f"starting with file {file_name}")
        print('starting upload to database')
        i = 0
        for index, row in df.iterrows():
            if i % 10000 == 0:
                print(f"rows imported: {i}")
            cursor.execute("INSERT INTO polish_salaries (code, place, quater, year, salary_brutto, currency, date) values(?,?,?,?,?,?,?)",
                           (row.code, row.place, row.quater, row.year, row.salary_brutto, row.currency, str(row.date)))
            i = i+1
        con.commit()
        print('upload success')
        con.close()
        print('connection closed')

if __name__ == '__main__':
    print('starting csv upload')
    df = download_from_csv_salaries.add_csv('csv_files/wynagrodzenia.csv')
    con, cursor = cs.sql_connect()
    download_from_csv_salaries.upload_data(con, cursor, df)

    print(df.head())

