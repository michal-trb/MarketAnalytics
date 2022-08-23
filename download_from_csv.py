import pandas as pd
import connect_sql as cs


def add_csv(link_csv):
    # upload csv file, drop unnesesery columns and NaN rows
    df = pd.read_csv(link_csv, sep=";")
    df.drop(['Atrybut', 'Unnamed: 9'], axis=1, inplace=True)
    df.dropna(inplace=True)

    # change column names and add column with date
    df.columns = ['code', 'place', 'quater', 'transactions', 'area', 'year', 'm2_value', 'unit']
    df['date'] = df['quater'].apply(change_quater)
    df['year'] = df['year'].apply(str)
    df['date'] = df['year'].str.cat(df['date'])
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    return df


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


def upload_data(con, cursor, df):
    print('starting upload to database')
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO polish_market (code, place, quater, transactions, area, year, m2_value, unit, date) values(?,?,?,?,?,?,?,?,?)",
                       (row.code, row.place, row.quater, row.transactions, row.area, row.year, row.m2_value, str(row.unit),str(row.date)))
    con.commit()
    print('upload success')
    con.close()
    print('connection closed')


if __name__ == '__main__':
    print('starting csv upload')
    df_polish_market = add_csv('RYNE_3794_CREL_20220811161137.csv')
    con, cursor = cs.sql_connect()
    upload_data(con, cursor, df_polish_market)

