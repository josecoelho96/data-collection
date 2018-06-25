#!/usr/bin/env python3

import logging
import argparse
import datetime
import json
import psycopg2
from psycopg2.extensions import AsIs
import os

from env import DB


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load database table with contents from JSON file.")
    parser.add_argument('input', help='Input JSON file name')
    parser.add_argument('table', help='Table name to load data with')

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


def load_json_file(filename):
    try:
        with open(filename, 'r') as f:
            content = json.load(f)
            logging.info("Loaded file '{}'.".format(filename))
            return content

    except Exception as e:
        logging.error("Error loading file '{}'. Details: {}.".format(filename, e))
        print("Error. See log for details.")
        exit(-1)


def load_table_data(db_conn, content, table_name):
    cursor = db_conn.cursor()
    SQL = """
        INSERT INTO %s (origin, date_created, temperature, humidity, light_intensity)
        VALUES (%s, %s, %s, %s, %s);
    """
    logging.info("Inserting {} rows into table '{}'.".format(content['summary']['count'], table_name))

    for row in content['measurements']:
        data = (AsIs(table_name),
            row['origin'],
            row['date_created'],
            row['temperature'],
            row['humidity'],
            row['light_intensity'],
        )
        try:
            cursor.execute(SQL, data)
        except Exception as e:
            logging.error("Failed to load row (date_created='{}')into database: {}".format(row['date_created'], e))
            print('Error. Check log for details.')

    logging.info("Data inserted.")


def main():
    args = parse_args()
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/json_to_db.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    logging.info('Starting...')

    connection = connect_database(DB['name'],
                                DB['user'],
                                DB['password'],
                                DB['host'],
                                DB['port'])

    content = load_json_file(args.input)
    load_table_data(connection, content, args.table)

    connection.close()
    logging.info('Done.')


if __name__ == "__main__":
    main()