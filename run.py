import shutil
import os
import clean


def delete_data_dir_contents():
    if os.path.exists('data'):
        shutil.rmtree('data')
    os.mkdir('data')


def scrap():
    os.system('scrapy crawl events -o data/events.json')
    os.system('scrapy crawl weapon_stats_by_event -o data/weapon_stats_by_event.json')


def main():
    delete_data_dir_contents()
    scrap()
    clean.main()


if __name__ == '__main__':
    main()
