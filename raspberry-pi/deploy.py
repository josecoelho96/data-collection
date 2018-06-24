#! /usr/bin/env python3

import psycopg2
from psycopg2.extensions import AsIs

from env import DB, TABLE_NAME


def connectDatabase(db_name, db_user, db_password, db_host, db_port):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        return cursor
    except Exception as e:
        print(e)
        return None

def createTable(db_cursor, table_name):
    SQL = """
        CREATE TABLE %s (
            id              SERIAL PRIMARY KEY,
            origin          CHAR(50) NOT NULL,
            date_created    TIMESTAMP NOT NULL,
            temperature     INT NOT NULL,
            humidity        INT NOT NULL,
            light_intensity INT NOT NULL
        );
    """
    data = (AsIs(table_name), )
    db_cursor.execute(SQL, data)

def dropTable(db_cursor, table_name):
    SQL = "DROP TABLE IF EXISTS %s;"
    data = (AsIs(table_name), )
    db_cursor.execute(SQL, data)

def main():
    cursor = connectDatabase(DB['name'], DB['user'], DB['password'], DB['host'], DB['port'])
    dropTable(cursor, TABLE_NAME)
    createTable(cursor, TABLE_NAME)

if __name__ == "__main__":
    main()