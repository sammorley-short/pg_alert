import logging
from pprint import pprint
from pg_alert.scrape import get_all_bookable_slots
from pg_alert.availability import check_availability
from pg_alert.sheets import read_signup_sheet
from pg_alert.io import save_to_json


def run():
    bookable_slots = get_all_bookable_slots()
    print(f"Bookable slots:")
    pprint(bookable_slots)

    signup_data = read_signup_sheet()
    print("Signup data:")
    pprint(signup_data)
    save_to_json(signup_data, 'signups.json')

    # example_data = {
    #     'Mon': ['08:00-14:00', '16:00-23:59'],
    #     'Tue': [],
    #     'Wed': ['06:00-22:00'],
    #     'Thu': [],
    #     'Fri': ['12:00-12:01'],
    #     'Sat': [],
    #     'Sun': ['16:00-23:00', '10:00-14:00'],
    # }

    # good_slots = check_availability(example_data, available_slots)
    # print("Good slots:")
    # pprint(good_slots)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger('selenium').setLevel(logging.WARNING)
    # logging.getLogger('urllib3').setLevel(logging.WARNING)
    run()
