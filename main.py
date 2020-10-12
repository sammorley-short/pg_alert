from datetime import date, timedelta
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.expected_conditions import presence_of_element_located


URL = "https://planetgranite.com"

GYMS_BOOKING_URLS = {
    "Belmont_roped": "https://app.rockgympro.com/b/widget/?a=offering&offering_guid=3786a62dd58b459abfadf82b7d2276d7&widget_guid=b7c6e7d4c2bd41b1a44990b9a402886c&random=5f7eb42886fc1&iframeid=&mode=p",  # noqa
}

XPATHS = {
    'date_selection_form': "/html/body/div[1]/div/form",
    'calendar': "/html/body/div[1]/div/form/div[6]/fieldset/div/div",
    'month_selector': "/html/body/div[1]/div/form/div[6]/fieldset/div/div/div",
    'day_table': "/html/body/div[1]/div/form/div[6]/fieldset/div/div/table/tbody",
    'table_row': ".//tr",
}

CLASSES = {
    'calendar': 'ui-datepicker-calendar',
    'available_date': "datepicker-available-day",
    'date': "ui-state-default",
}

IDS = {
    'schedule': "offering-page-select-events-table",
}

MAX_WAIT_SECONDS = 3


def run():
    booking_url = GYMS_BOOKING_URLS['Belmont_roped']
    driver = setup_driver(booking_url)
    available_slots = get_available_slots(driver)

    print(f"Available slots:")
    pprint(available_slots)

    driver.save_screenshot('screenshot.png')
    driver.quit()


def setup_driver(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(MAX_WAIT_SECONDS)
    driver.get(url)

    # Explicit wait code below
    # wait = WebDriverWait(driver, MAX_WAIT_SECONDS)

    return driver


def get_available_slots(driver):
    bookable_day_elements = get_bookable_date_elements(driver)

    available_slots = []
    for bookable_day_element in bookable_day_elements:
        print(bookable_day_element.text)
        available_slots += get_available_slots_for_date(driver, bookable_day_element)
        print(available_slots)

    return available_slots


def get_bookable_date_elements(driver):
    """ Returns a generator over bookable date elements. """
    # TODO: Add ability to skip forward a month if needed

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
    day_element.click()
    return get_available_schedule_slots(driver)


def get_available_schedule_slots(driver):
    available_slots = []
    schedule_element = driver.find_element_by_id(IDS['schedule'])
    for row in schedule_element.find_elements_by_xpath(XPATHS['table_row']):
        slot_element = row.find_elements_by_xpath(".//td")
        if is_available_slot(slot_element):
            available_slots.append(slot_element[0].text)

    return available_slots


def is_available_slot(slot_element):
    return slot_element[-1].text == "Select"


if __name__ == '__main__':
    run()
