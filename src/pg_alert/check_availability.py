from pprint import pprint


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
