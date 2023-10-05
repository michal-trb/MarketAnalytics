from download_from_csv_salaries import download_from_csv_salaries as salaries
from download_from_csv import download_from_csv as dims
from download_from_csv_values import download_from_csv_values as values
from create_database import create_database

import connect_sql as cs
import os

os.remove('Market.db')

create_database()


df_median_house_price = dims.add_csv('csv_files/mediana_cen_mieszkan.csv')
con, cursor = cs.sql_connect()
dims.upload_data(con, cursor, df_median_house_price, 'csv_files/mediana_cen_mieszkan.csv')

df_sum_value = values.add_csv('csv_files/mediana_cen_mieszkan.csv')
con, cursor = cs.sql_connect()
values.upload_data(con, cursor, df_sum_value, "fact_polish_market_median_m2", 'csv_files/mediana_cen_mieszkan.csv')

df_sum_value = values.add_csv('csv_files/suma_wart_sprzed.csv')
con, cursor = cs.sql_connect()
values.upload_data(con, cursor, df_sum_value, "fact_polish_market_sum_value", 'csv_files/suma_wart_sprzed.csv')

df_count = values.add_csv('csv_files/suma_transakcji.csv')
con, cursor = cs.sql_connect()
values.upload_data(con, cursor, df_count, "fact_polish_market_count", 'csv_files/suma_transakcji.csv')

df_count_m2 = values.add_csv('csv_files/suma_m2.csv')
con, cursor = cs.sql_connect()
values.upload_data(con, cursor, df_count_m2, "fact_polish_market_count_m2", 'csv_files/suma_m2.csv')

df_salaries = salaries.add_csv('csv_files/wynagrodzenia.csv')
con, cursor = cs.sql_connect()
salaries.upload_data(con, cursor, df_salaries, 'csv_files/wynagrodzenia.csv')