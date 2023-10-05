import io
import sys
from connect_sql import sql_connect
import pytest
import sqlite3

def test_sql_connect_raises_exception():
    with pytest.raises(Exception):
        sql_connection = "DRIVER={SQLite3 ODBC Driver};SERVER=nonexistent;DATABASE=NonexistentDB.db;Trusted_connection=yes"
        con, cursor = sql_connect(sql_connection)

def test_sql_connect_returns_connection_and_cursor():
    con, cursor = sql_connect()
    assert con is not None
    assert cursor is not None
    con.close()

def test_sql_connect_returns_correct_types():
    con, cursor = sql_connect()
    assert isinstance(con, sqlite3.Connection)
    assert isinstance(cursor, sqlite3.Cursor)
    con.close()


