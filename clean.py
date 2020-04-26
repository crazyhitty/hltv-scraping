# -*- coding: utf-8 -*-
from os import path
import json


def main():
    weapon_stats_json_path = 'data/weapon_stats_by_event.json'

    if not path.exists(weapon_stats_json_path):
        print(weapon_stats_json_path, 'does not exist')
        return

    with open(weapon_stats_json_path, 'r') as json_file:
        json_data = json.load(json_file)
        stats = {}
        for json_item in json_data:
            # Find total value for calculating percentage.
            total = 0
            for weapon_stats in json_item['weapon_stats']:
                total += float(weapon_stats['value'])

            # Calculate each weapon usage percentage.
            for weapon_stats in json_item['weapon_stats']:
                individual_weapon_stat = {
                    'event_id': json_item['event_id'],
                    'event_name': json_item['event_name'],
                    'event_start_date': json_item['event_start_date'],
                    'event_end_date': json_item['event_end_date'],
                    'value': float(weapon_stats['value']) * 100 / total
                }
                if weapon_stats['label'] in stats.keys():
                    stats[weapon_stats['label']].append(individual_weapon_stat)
                else:
                    stats[weapon_stats['label']] = [individual_weapon_stat]

        with open('data/weapon_stats_final.json', 'w') as weapon_stats_final_file:
            json.dump(stats, weapon_stats_final_file)

        print(stats)


if __name__ == '__main__':
    main()
