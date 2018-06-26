#!/usr/bin/env python3

import argparse
import datetime
import json
import logging
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find missing readings (gaps) from a JSON file.")
    parser.add_argument('input', help='Input JSON file name')
    parser.add_argument('output_gaps', help='Output gaps list file')
    parser.add_argument('output_duplicates', help='Output duplicates list file')
    parser.add_argument('output_json', help='Output JSON measurements file')

    return parser.parse_args()


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


def get_equivalent_minutes(start_dt, current_dt):

    start = start_dt.replace(second=0, microsecond=0)
    current = current_dt.replace(second=0, microsecond=0)

    gap = (current - start)
    return gap.days * 1440 + gap.seconds//60



def list_faults(content, gaps, duplicates):

    summary = content['summary']
    measurements = content['measurements']

    start_timestamp = datetime.datetime.strptime(summary['start_timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    end_timestamp = datetime.datetime.strptime(summary['end_timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    measurements_delta = end_timestamp - start_timestamp

    logging.info("Analyzing {} measurements: '{}' [from '{}' to '{}'].".
        format(
            summary['count'],
            measurements_delta,
            summary['start_timestamp'],
            summary['end_timestamp']
        )
    )

    start_measurement = measurements[0]
    last_measurement = start_measurement
    last_timestamp = datetime.datetime.strptime(last_measurement['date_created'], "%Y-%m-%d %H:%M:%S.%f")
    last_v = get_equivalent_minutes(start_timestamp, last_timestamp)

    for m in measurements[1:]:
        current_timestamp = datetime.datetime.strptime(m['date_created'], "%Y-%m-%d %H:%M:%S.%f")
        v = get_equivalent_minutes(start_timestamp, current_timestamp)

        if v - last_v == 0:
            # Duplicate
            measurement_label = datetime.datetime.strftime(last_timestamp,  "%Y-%m-%d %H:%M")
            # original_ts_str = datetime.datetime.strftime(last_timestamp,  "%Y-%m-%d %H:%M")
            # duplicate_ts_str = datetime.datetime.strftime(current_timestamp,  "%Y-%m-%d %H:%M")
            logging.warn("A duplicate was was found for measurement '{}'. Original: '{}'. Duplicate: '{}'".
                format(measurement_label, last_timestamp, current_timestamp)
            )

            # Do the measurements have the same values?
            if last_measurement['origin'] == m['origin'] and \
                last_measurement['temperature'] == m['temperature'] and \
                last_measurement['humidity'] == m['humidity'] and \
                last_measurement['light_intensity'] == m['light_intensity']:
                logging.info("Measurements have the same values. Removed the last one.")
                # Remove current measurement
                measurements.remove(m)
            else:
                logging.error("Measurements have different values. Added to list of duplicates.")
                print("Duplicate for '{}' with different values found. Check log and output file for details.".format(measurement_label))
                duplicates.append(str(measurement_label)+' | ' + str(last_timestamp) + ' | ' + str(current_timestamp) +  ' | MANUAL_FIX')

            continue
        elif v - last_v > 1:
            # Gap
            gap_size = v - last_v - 1
            time_delta = datetime.timedelta(minutes=1)
            gap_start = last_timestamp.replace(second=0, microsecond=0) + time_delta
            gap_end = current_timestamp.replace(second=0, microsecond=0) - time_delta
            gap_start_str = datetime.datetime.strftime(gap_start, "%Y-%m-%d %H:%M")
            gap_end_str = datetime.datetime.strftime(gap_end, "%Y-%m-%d %H:%M")

            if gap_size == 1:
                logging.warn("A gap was was found. Dimension: {} ['{}']".
                    format(gap_size, gap_start_str)
                )
                gaps.append(datetime.datetime.strftime(gap_start, "%Y-%m-%d %H:%M"))
            else:
                logging.warn("A gap was was found. Dimension: {} ['{}' to '{}']".
                    format(gap_size, gap_start_str, gap_end_str)
                )
                while gap_start <= gap_end:
                    gaps.append(datetime.datetime.strftime(gap_start, "%Y-%m-%d %H:%M"))
                    gap_start = gap_start + datetime.timedelta(minutes=1)

        last_v = v
        last_measurement = m
        last_timestamp = current_timestamp

    # Update summary on dictionary
    content['summary']['count'] = len(content['measurements'])


def save_gaps_list(content, filename):
    logging.info("Saving gaps to output file '{}'.".format(filename))
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            for line in content:
                f.write("{}\n".format(line))

    except Exception as e:
        logging.error('Failed to save to file: {}'.format(e))
        print('Error. See log for details.')
        exit(-1)


def save_duplicates_list(content, filename):
    logging.info("Saving duplicates to output file '{}'.".format(filename))
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            for line in content:
                f.write("{}\n".format(line))

    except Exception as e:
        logging.error('Failed to save to file: {}'.format(e))
        print('Error. See log for details.')
        exit(-1)


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
    logging.basicConfig(filename='logs/find_gaps_duplicates.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    logging.info('Starting...')

    content = load_json_file(args.input)
    gaps = []
    duplicates = []
    list_faults(content, gaps, duplicates)
    save_gaps_list(gaps, args.output_gaps)
    save_duplicates_list(duplicates, args.output_duplicates)
    save_json(content, args.output_json)

    logging.info('Done.')


if __name__ == "__main__":
    main()
