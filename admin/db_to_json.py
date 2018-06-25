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
        description="Get database table contents into JSON format.")
    parser.add_argument('output', help='Output file name')
    parser.add_argument('table', help='Table name to retrieve data from')

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


def get_table_data(db_conn, table_name):

    results = {}
    cursor = db_conn.cursor()
    SQL = """
        SELECT origin, date_created, temperature, humidity, light_intensity
        FROM %s
        ORDER BY date_created ASC;
    """
    data = (AsIs(table_name), )
    try:
        cursor.execute(SQL, data)
    except Exception as e:
        logging.critical('Failed to retrieve data from database: {}'.format(e))
        exit(-1)

    count = cursor.rowcount
    logging.info("Got {} measurements from table '{}'.".format(count, table_name))
    results['summary'] = {
        'count': count
    }
    results['measurements'] = []

    rows = cursor.fetchall()
    for row in rows:
        results['measurements'].append({
            'date_created': datetime.datetime.strftime(row[1], "%Y-%m-%d %H:%M:%S.%f"),
            'origin': row[0].strip(),
            'temperature': row[2],
            'humidity': row[3],
            'light_intensity': row[4]
        })

    results['summary'] = {
        'count': count,
        'start_timestamp': datetime.datetime.strftime(rows[0][1], "%Y-%m-%d %H:%M:%S.%f"),
        'end_timestamp': datetime.datetime.strftime(rows[-1][1], "%Y-%m-%d %H:%M:%S.%f")
    }

    cursor.close()
    return results


def save_json(content, file):
    logging.info("Saving JSON to output file '{}'.".format(file))

    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w') as f:
            json.dump(content, f, indent=2)
    except Exception as e:
        logging.error('Failed to save to file: {}'.format(e))
        print('Error. See log for details.')
        exit(-1)


def main():
    args = parse_args()
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/db_to_json.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    logging.info('Starting...')

    connection = connect_database(DB['name'],
                                DB['user'],
                                DB['password'],
                                DB['host'],
                                DB['port'])

    results = get_table_data(connection, args.table)
    save_json(results, args.output)
    connection.close()
    logging.info('Done.')


if __name__ == "__main__":
    main()