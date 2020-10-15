import logging
from dateutil.parser import parse
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

log = logging.getLogger(__name__)

GYMS_BOOKING_URLS = {
    "Belmont_roped": "https://app.rockgympro.com/b/widget/?a=offering&offering_guid=3786a62dd58b459abfadf82b7d2276d7&widget_guid=b7c6e7d4c2bd41b1a44990b9a402886c&random=5f7eb42886fc1&iframeid=&mode=p",  # noqa
}

XPATHS = {
    'table_row': ".//tr",
    'table_row_data': ".//td",
}

CLASSES = {
    'calendar': 'ui-datepicker-calendar',
    'available_date': "datepicker-available-day",
    'date': "ui-state-default",
    'next_month': "ui-datepicker-next",
    'year': 'ui-datepicker-year',
}

IDS = {
    'schedule': "offering-page-select-events-table",
}

MAX_WAIT_SECONDS = 5

MAX_SPACES = 15


def get_all_available_slots():
    booking_url = GYMS_BOOKING_URLS['Belmont_roped']
    driver = setup_driver(booking_url)

    # Get any available dates in this month and the next
    available_slots = get_available_slots_for_current_month(driver)
    advance_month(driver)
    available_slots += get_available_slots_for_current_month(driver)

    driver.quit()
    return available_slots


def setup_driver(url):
    log.debug(f"Setting up driver for URL:\n{url}")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(MAX_WAIT_SECONDS)
    driver.get(url)
    return driver


def get_available_slots_for_current_month(driver):
    log.debug("Getting available slots for current month. ")
    bookable_day_elements = get_bookable_date_elements(driver)

    available_slots = []
    for bookable_day_element in bookable_day_elements:
        available_slots += get_available_slots_for_date(driver, bookable_day_element)

    return available_slots


def get_bookable_date_elements(driver):
    """ Returns a generator over bookable date elements. """
    log.debug("Getting all bookable dates.")
    yielded_dates = []
    while True:
        available = driver.find_elements_by_class_name(CLASSES['available_date'])
        date_elements = (
            element.find_element_by_class_name(CLASSES['date'])
            for element in available
        )
        try:
            date_element = next(filter(lambda e: e.text not in yielded_dates, date_elements))
        except StopIteration:
            break
        yielded_dates.append(date_element.text)
        yield date_element


def get_available_slots_for_date(driver, day_element):
    log.debug(f"Clicking on day {day_element.text}.")
    day_element.click()
    return get_available_schedule_slots(driver)


def get_available_schedule_slots(driver):
    log.debug("Getting all available schedule slots for date.")
    year = get_year(driver)
    available_slots = []
    schedule_element = driver.find_element_by_id(IDS['schedule'])
    for row in schedule_element.find_elements_by_xpath(XPATHS['table_row']):
        slot_data_elements = row.find_elements_by_xpath(XPATHS["table_row_data"])
        if is_available_slot(slot_data_elements):
            slot = make_slot(slot_data_elements, year)
            available_slots.append(slot)

    return available_slots


def get_year(driver):
    year_element = driver.find_element_by_class_name(CLASSES['year'])
    return year_element.text


def is_available_slot(slot_data_elements):
    return slot_data_elements[-1].text == "Select"


Slot = namedtuple("Slot", ['date', 'start_time', 'end_time', 'num_spaces'])


def make_slot(slot_data_elements, year):
    time_element, availability_element, *_ = slot_data_elements
    date, start_time, end_time = parse_slot_time_element(time_element, year)
    num_spaces = parse_slot_availability_element(availability_element)
    return Slot(date, start_time, end_time, num_spaces)


def parse_slot_time_element(time_element, year):
    time_data = time_element.text
    weekday, month_date, time_range = time_data.split(', ')
    start_time, end_time = time_range.split(' to ')

    start_timedate = parse(' '.join([start_time, month_date, year]))
    end_timedate = parse(' '.join([end_time, month_date, year]))
    return start_timedate.date(), start_timedate.time(), end_timedate.time()


def parse_slot_availability_element(availability_element):
    availability_data = availability_element.text
    _, spaces = availability_data.split('\n')
    if spaces == 'Available':
        return MAX_SPACES
    else:
        return int(spaces.split(' ')[0])


def advance_month(driver):
    log.debug("Advancing one month.")
    next_month_button = driver.find_element_by_class_name(CLASSES['next_month'])
    next_month_button.click()
