import pandas as pd
import connect_sql as cs
import unicodedata

class download_from_csv_salaries:
    
    @staticmethod
    def add_csv(link_csv):
        # upload csv file, drop unnesesery columns and NaN rows
        df = pd.read_csv(link_csv, sep=";", engine='python')
        df.drop(['Wynagrodzenie brutto','Atrybut', 'Unnamed: 8'], axis=1, inplace=True)
        df.dropna(inplace=True)

        # change column names and add column with date
        df.columns = ['code', 'place', 'quater', 'year', 'salary_brutto', 'currency']
        df['date'] = df['quater'].apply(download_from_csv_salaries.change_quater)
        df['year'] = df['year'].apply(str)
        df['date'] = df['year'].str.cat(df['date'])
        df['code'] = df['place'].str.replace('\s+', '').str.upper().str.replace('-', '') + df['date'].str.replace('-', '')
        df['code'] = df['code'].apply(download_from_csv_salaries.remove_polish_chars)
        df['date'] = pd.to_datetime(df['date'])
        df['salary_brutto'] = df['salary_brutto'].replace(',','.', regex=True)
        df.sort_values('date', inplace=True)
        return df

    @staticmethod
    def remove_polish_chars(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    @staticmethod
    def upload_data(con, cursor, df):
        print('starting upload to database')
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO polish_salaries (code, place, quater, year, salary_brutto, currency, date) values(?,?,?,?,?,?,?)",
                           (row.code, row.place, row.quater, row.year, row.salary_brutto, row.currency, str(row.date)))
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
    df = add_csv('wynagrodzenia.csv')
    con, cursor = cs.sql_connect()
    upload_data(con, cursor, df)

    print(df.head())

