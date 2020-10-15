import logging
from pprint import pprint
from pg_alert.get_slots import get_all_available_slots
from pg_alert.check_availability import check_availability


def run():
    available_slots = get_all_available_slots()

    print(f"Available slots:")
    pprint(available_slots)

    example_data = {
        'Mon': ['08:00-14:00', '16:00-24:00'],
        'Tue': [],
        'Wed': ['06:00-22:00'],
        'Thu': [],
        'Fri': ['12:00-12:01'],
        'Sat': [],
        'Sun': ['16:00-23:00', '10:00-14:00'],
    }

    check_availability(example_data, available_slots)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    run()
