import pandas as pd
import connect_sql as cs
import unicodedata

class download_from_csv:

    @staticmethod
    def add_csv(link_csv):
        # upload csv file, drop unnesesery columns and NaN rows
        df = pd.read_csv(link_csv, sep=";")
        df.drop(['Atrybut', 'Unnamed: 9', 'Wartosc', 'Jednostka miary'], axis=1, inplace=True)
        df.dropna(inplace=True)

        # change column names and add column with date
        df.columns = ['code', 'place', 'quater', 'transactions', 'area', 'year']
        df['date'] = df['quater'].apply(download_from_csv.change_quater)
        df['year'] = df['year'].apply(str)
        df['date'] = df['year'].astype(str).str.cat(df['date'])
        df = download_from_csv.create_code(df)
        df = download_from_csv.create_salary_code(df)
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        return df

    @staticmethod
    def create_code(df):
        df['code'] = df['place'].str.replace('\s+', '').str.upper().str.replace('-', '') + df['date'].str.replace('-', '')
        df['code'] += df['area'].str.replace('\s+', '').str.replace(',', '').replace(' ', '')
        df['code'] += df['transactions'].replace('\s+', '').replace('rynek pierwotny', 'rp').replace('rynek wtórny', 'rw').replace('ogółem', 'o')
        df['code'] = df['code'].apply(download_from_csv.remove_polish_chars)
        return df

    def create_salary_code(df):
        df['salary_code'] = df['place'].str.replace('\s+', '').str.upper().str.replace('-', '') + df['date'].str.replace('-', '')
        df['salary_code'] = df['salary_code'].apply(download_from_csv.remove_polish_chars)
        return df

    @staticmethod
    def remove_polish_chars(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    @staticmethod
    def upload_data(con, cursor, df, file_name):
        print(f"starting with file {file_name}")
        print('starting upload to database')
        i = 0
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO dim_polish_market (code, salary_code, place, quater, transactions, area, year, date) values(?,?,?,?,?,?,?,?)",
                           (row.code, row.salary_code, row.place, row.quater, row.transactions, row.area, row.year, str(row.date)))
            if i % 10000 == 0:
                print(f"rows imported: {i}")
            i = i+1
        con.commit()
        print('upload success')
        con.close()
        print('connection closed')
    
    @staticmethod
    def change_quater(s):
        if s == '1 kwartał':
            return '-01-01'
        elif s == '2 kwartał':
            return '-04-01'
        elif s == '3 kwartał':
            return '-07-01'
        elif s == '4 kwartał':
            return '-10-01'
        return ''

if __name__ == '__main__':
    print('starting csv upload')
    df_polish_market = download_from_csv.add_csv('csv_files/mediana_cen_mieszkan.csv')
    con, cursor = cs.sql_connect()
    download_from_csv.upload_data(con, cursor, df_polish_market)
    print(df_polish_market.head())