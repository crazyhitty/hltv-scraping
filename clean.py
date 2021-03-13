# -*- coding: utf-8 -*-

from os import path
import json
from datetime import datetime


def format_monthly_data(json_data):
    # Sort data by end date in ascending order.
    sorted_json_data = sorted(json_data, key=lambda items: items['end_date'])

    monthly_stats = {}

    for json_item in sorted_json_data:
        # Calculate summation of all weapon usage values for single date range.
        # This total will be used to calculate individual weapon usage percentage for this date range.
        total = 0
        for weapon_stats in json_item['weapon_stats']:
            total += float(weapon_stats['value'])

        if total == 0:
            # Looks like no weapon data is available for this date range ; skipping processing of this date range.
            continue

        end_date_timestamp = datetime.strptime(json_item['end_date'], '%Y-%m-%d').timestamp()

        # Calculate each weapon usage percentage.
        for weapon_stats in json_item['weapon_stats']:
            weapon_usage_percentage = float(weapon_stats['value']) * 100 / total

            if weapon_stats['label'] in monthly_stats.keys():
                monthly_stats[weapon_stats['label']].append({
                    'date': end_date_timestamp,
                    'value': weapon_usage_percentage
                })
            else:
                monthly_stats[weapon_stats['label']] = [{
                    'date': end_date_timestamp,
                    'value': weapon_usage_percentage
                }]

    return monthly_stats


def main():
    weapon_stats_json_path = 'data/weapon_stats_per_month.json'

    if not path.exists(weapon_stats_json_path):
        print(weapon_stats_json_path, 'does not exist')
        return

    with open(weapon_stats_json_path, 'r') as json_file:
        json_data = json.load(json_file)

        monthly_stats = format_monthly_data(json_data)

        with open('data/weapon_stats_per_month_formatted.json', 'w') as weapon_stats_monthly_formatted_file:
            json.dump(monthly_stats, weapon_stats_monthly_formatted_file)


if __name__ == '__main__':
    main()
