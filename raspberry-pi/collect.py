#! /usr/bin/env python3

import psycopg2
import time
import serial
from datetime import datetime
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

def insertData(db_cursor, db_table, values):
    SQL = """INSERT INTO %s (
                    origin,
                    date_created,
                    temperature,
                    humidity,
                    light_intensity
                ) VALUES (%s, %s, %s, %s, %s)"""
    data = (AsIs(db_table),
                values['origin'],
                values['date_created'],
                values['temperature'],
                values['humidity'],
                values['light_intensity']
            )
    db_cursor.execute(SQL, data)

def connectSerial():
    # Raspberry Pi 1
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        xonxoff = False,
        rtscts = False,
        dsrdtr = False,
        timeout = 10
    )
    # Waiting to be stable
    time.sleep(4)
    return ser

def getSensorData(ser):
    values = {}
    ser.write('1'.encode())
    raw_data = ser.readline().decode()
    data = raw_data[:-2].split('|')
    values['origin'] = 'C206'
    values['date_created'] = datetime.now()
    for element in data:
        if element[0] == 'L':
            values['light_intensity'] = element[2:]
        elif element[0] == 'T':
            values['temperature'] = element[2:]
        elif element[0] == 'H':
            values['humidity'] = element[2:]
    return values

def main():
    # Connect to database
    cursor = connectDatabase(DB['name'], DB['user'], DB['password'], DB['host'], DB['port'])
    # Get data from arduino
    ser = connectSerial()
    values = getSensorData(ser)
    # Insert data into database
    insertData(cursor, TABLE_NAME, values)

if __name__ == "__main__":
    main()







