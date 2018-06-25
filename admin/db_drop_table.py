#!/usr/bin/env python3

import argparse
import logging
import psycopg2
from psycopg2.extensions import AsIs
import os

from env import DB


def parse_args():
    parser = argparse.ArgumentParser(
        description="Drop a table in a database.")

    parser.add_argument('table', help='Table to create name')
    return parser.parse_args()


def connect_database(db_name, db_user, db_password, db_host, db_port):
    logging.info('Connecting to database...')
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        logging.info('Connected to database.')
        return conn
    except Exception as e:
        logging.critical('Failed to connect to database: {}'.format(e))
        print('Error. See log for details.')
        exit(-1)


def drop_table(db_conn, table_name):


    cursor = db_conn.cursor()
    SQL = """
        DROP TABLE IF EXISTS %s;
    """
    data = (AsIs(table_name), )
    try:
        cursor.execute(SQL, data)
    except Exception as e:
        logging.critical("Failed to drop table: '{}'".format(e))
        print('Error. See log for details.')
        exit(-1)
    logging.info("Table '{}' droped.".format(table_name))
    cursor.close()


def main():
    args = parse_args()
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/db_drop_table.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    logging.info('Starting...')
    connection = connect_database(DB['name'],
                                DB['user'],
                                DB['password'],
                                DB['host'],
                                DB['port'])

    drop_table(connection, args.table)
    connection.close()
    logging.info('Done.')


if __name__ == "__main__":
    main()