import logging
from pprint import pprint
from pg_alert.scrape import get_all_bookable_slots
from pg_alert.availability import find_attendable_slots
from pg_alert.sheets import read_signup_sheet
from pg_alert.io import save_to_json
from pg_alert.errors import UnsupportedGym


def run():
    # Read the sign-up data and then dump it to a JSON
    signup_data = read_signup_sheet()
    save_to_json(signup_data, 'signups.json')
    print("Signup data:")
    pprint(signup_data)

    # Compile list of attendable slots
    all_attendable_slots = {}
    for gym_name, gym_signups in signup_data.items():
        try:
            bookable_slots = get_all_bookable_slots(gym_name)
        except UnsupportedGym:
            print(f"Skipping unknown gym {gym_name}")
            continue
        print(f"Bookable slots for {gym_name}:")
        pprint(bookable_slots)

        for gym_signup in gym_signups:
            name = gym_signup['name']
            email = gym_signup['email']
            availability = gym_signup['availability']
            attendable_slots = find_attendable_slots(availability, bookable_slots)
            if attendable_slots:
                all_attendable_slots.setdefault((name, email), {})
                all_attendable_slots[(name, email)][gym_name] = attendable_slots

            print(f"User {name} can attend slots:")
            print(attendable_slots)

    print(all_attendable_slots)

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
