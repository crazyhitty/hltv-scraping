# -*- coding: utf-8 -*-

from os import path
import json
from datetime import datetime

def format_data_monthly_avg(json_data):
    # Sort data by event end date in ascending order.
    sorted_json_data = sorted(json_data, key=lambda items: int(items['event_end_date']))

    monthly_grouped_stats = {}

    for json_item in sorted_json_data:
        # Calculate summation of all weapon usage values in this event.
        # This total will be used to calculate individual weapon usage percentage in this event.
        total = 0
        for weapon_stats in json_item['weapon_stats']:
            total += float(weapon_stats['value'])

        if total == 0:
            # Looks like no weapon data is available for this event ; skipping processing of this event.
            continue

        event_end_date = float(json_item['event_end_date']) / 1000  # Event end date in epoch seconds.
        event_end_date_mm_yyyy = datetime.fromtimestamp(event_end_date).strftime("%m-%Y")

        # Calculate each weapon usage percentage.
        for weapon_stats in json_item['weapon_stats']:
            weapon_usage_percentage = float(weapon_stats['value']) * 100 / total

            # Group monthly weapon data which will be used to calculate monthly weapon usage avg.
            # {
            #     "weapon_name": {
            #         "mm_yyyy": {
            #             "total": number,
            #             "count": number
            #         },
            #         ...
            #     },
            #     ...
            # }
            if weapon_stats['label'] in monthly_grouped_stats.keys():
                if event_end_date_mm_yyyy in monthly_grouped_stats[weapon_stats['label']].keys():
                    monthly_grouped_stats[weapon_stats['label']][event_end_date_mm_yyyy]['total'] += weapon_usage_percentage
                    monthly_grouped_stats[weapon_stats['label']][event_end_date_mm_yyyy]['count'] += 1
                else:
                    monthly_grouped_stats[weapon_stats['label']][event_end_date_mm_yyyy] = {
                        'total': weapon_usage_percentage,
                        'count': 1,
                    }
            else:
                monthly_grouped_stats[weapon_stats['label']] = {
                    event_end_date_mm_yyyy: {
                        'total': weapon_usage_percentage,
                        'count': 1,
                    }
                }

    monthly_avg_stats = {}

    # Calculate monthly average from grouped data
    for weapon_label in monthly_grouped_stats.keys():
        for mm_yyyy in monthly_grouped_stats[weapon_label].keys():
            total = monthly_grouped_stats[weapon_label][mm_yyyy]['total']
            count = monthly_grouped_stats[weapon_label][mm_yyyy]['count']
            avg = total / count
            timestamp = datetime.strptime(mm_yyyy, '%m-%Y').timestamp()
            if weapon_label in monthly_avg_stats.keys():
                monthly_avg_stats[weapon_label].append({
                    'date': timestamp,
                    'value': avg
                })
            else:
                monthly_avg_stats[weapon_label] = [{
                    'date': timestamp,
                    'value': avg
                }]

    return monthly_avg_stats


def main():
    weapon_stats_json_path = 'data/weapon_stats_by_event.json'

    if not path.exists(weapon_stats_json_path):
        print(weapon_stats_json_path, 'does not exist')
        return

    with open(weapon_stats_json_path, 'r') as json_file:
        json_data = json.load(json_file)

        monthly_avg_stats = format_data_monthly_avg(json_data)

        with open('data/weapon_stats_monthly_avg.json', 'w') as weapon_stats_monthly_avg_file:
            json.dump(monthly_avg_stats, weapon_stats_monthly_avg_file)


if __name__ == '__main__':
    main()
