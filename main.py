import logging
from pprint import pprint
from pg_alert.get_slots import get_all_available_slots
from pg_alert.check_availability import check_availability
from pg_alert.sheets import read_sheet


def run():
    available_slots = get_all_available_slots()

    print(f"Available slots:")
    pprint(available_slots)

    example_data = {
        'Mon': ['08:00-14:00', '16:00-23:59'],
        'Tue': [],
        'Wed': ['06:00-22:00'],
        'Thu': [],
        'Fri': ['12:00-12:01'],
        'Sat': [],
        'Sun': ['16:00-23:00', '10:00-14:00'],
    }

    good_slots = check_availability(example_data, available_slots)
    pprint(good_slots)


def sheet_run():
    sheet_id = get_sheet_id()
    sheet_data = read_sheet(sheet_id)
    pprint(sheet_data)


def get_sheet_id():
    with open('SHEET_ID', 'r') as file:
        return file.read().splitlines()[0]


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger('selenium').setLevel(logging.WARNING)
    # logging.getLogger('urllib3').setLevel(logging.WARNING)
    # run()
    sheet_run()
