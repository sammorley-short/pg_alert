from pprint import pprint
from pg_alert.get_slots import get_all_available_slots


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


def check_availability(desired_windows, available_slots):
    weekday_slots = sort_slots_by_weekday(available_slots)
    pprint(weekday_slots)
    assert False


def sort_slots_by_weekday(available_slots):
    weekday_slots = {
        'Mon': [],
        'Tue': [],
        'Wed': [],
        'Thu': [],
        'Fri': [],
        'Sat': [],
        'Sun': [],
    }
    for slot in available_slots:
        weekday = slot.date.strftime("%a")
        weekday_slots[weekday].append(slot)

    return weekday_slots


if __name__ == '__main__':
    run()
