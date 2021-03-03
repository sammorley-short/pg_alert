from pprint import pprint
from datetime import time
from collections import namedtuple
from .constants import WEEKDAYS


def check_availability(desired_windows, available_slots):
    weekday_slots = sort_slots_by_weekday(available_slots)
    weekday_windows = parse_desired_windows(desired_windows)
    pprint(weekday_slots)
    good_slots = []
    for weekday in WEEKDAYS:
        windows = weekday_windows[weekday]
        slots = weekday_slots[weekday]
        good_slots += check_weekday_availability(windows, slots)

    return good_slots


def sort_slots_by_weekday(available_slots):
    weekday_slots = {weekday: [] for weekday in WEEKDAYS}
    for slot in available_slots:
        weekday = slot.date.strftime("%a")
        weekday_slots[weekday].append(slot)

    return weekday_slots


def parse_desired_windows(desired_windows):
    return {weekday: parse_windows(windows) for weekday, windows in desired_windows.items()}


def parse_windows(windows):
    return [parse_window(window) for window in windows]


def parse_window(window):
    start_time, end_time = window.split('-')
    start_time = time.fromisoformat(start_time)
    end_time = time.fromisoformat(end_time)
    return Window(start_time, end_time)


Window = namedtuple('Window', ['start_time', 'end_time'])


def check_weekday_availability(windows, slots):
    # TODO: This can be done much more efficiently, but the problem size is too small for better implementation
    available_slots = []
    for slot in slots:
        for window in windows:
            if slot_inside_window(slot, window):
                available_slots.append(slot)
    return available_slots


def slot_inside_window(slot, window):
    return slot.start_time >= window.start_time and slot.end_time <= window.end_time
