# Planet Granite Alerter

This app is designed to alert users when desired slots become bookable at Planet Granite.
This is performed by the following steps:

1) Scrape the Planet Granite booking page to get all bookable slots (see `scrape.get_all_bookable_slots`)
2) Fetch each user's desired slots (and email) from a Google Sheets page (see `sheets.read_signup_sheet`)
3) Cross-reference bookable slots with desired slots to identify availability (see `availability.check_availability`)
4) Email each user with the set of eligbile slots (not yet implemented).
5) Repeat above steps every T minutes and remember which eligbile slots users have already been notified of (not yet implemented).

## Installation

To install for development, use 

`pip install .`

where the flag `-e` should be added when installing for development.
