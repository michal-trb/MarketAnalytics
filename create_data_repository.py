from download_from_csv_salaries import download_from_csv_salaries as dfcs
from download_from_csv import download_from_csv as dfc
import connect_sql as cs
import os
from create_database import create_database

os.remove('Market.db')

create_database()

salaries = dfcs()
median_house_price = dfc()

df_salaries = salaries.add_csv('csv_files/wynagrodzenia.csv')
con, cursor = cs.sql_connect()
salaries.upload_data(con, cursor, df_salaries)

df_median_house_price = median_house_price.add_csv('csv_files/mediana_cen_mieszkan.csv')
con, cursor = cs.sql_connect()
median_house_price.upload_data(con, cursor, df_median_house_price)

