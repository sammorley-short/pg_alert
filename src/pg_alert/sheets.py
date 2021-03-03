import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from .constants import WEEKDAYS

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
CELL_RANGE = 'A3:I'


def read_signup_sheet():
    sheet_id = get_sheet_id()
    return read_google_spreadsheet(sheet_id)


def get_sheet_id():
    with open('SHEET_ID', 'r') as file:
        return file.read().splitlines()[0]


def read_google_spreadsheet(sheet_id):
    creds = read_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    spreadsheet_data = sheet.get(spreadsheetId=sheet_id).execute()
    sheet_names = get_sheet_names(spreadsheet_data)
    spreadsheet_data = {}
    for sheet_name in sheet_names:
        range = f"'{sheet_name}'!{CELL_RANGE}"
        sheet_data = sheet.values().get(
            spreadsheetId=sheet_id,
            range=range
        ).execute()
        spreadsheet_data[sheet_name] = parse_sheet_data(sheet_data)
    return spreadsheet_data


def read_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_sheet_names(spreadsheet_data):
    sheets_metadata = spreadsheet_data['sheets']
    return [get_sheet_name(sheet_metadata) for sheet_metadata in sheets_metadata]


def get_sheet_name(sheet_metadata):
    return sheet_metadata['properties']['title']


def parse_sheet_data(sheet_data):
    data_rows = filter(is_valid_row, sheet_data['values'])
    return [
        parse_sheet_data_row(row)
        for row in data_rows
    ]


def is_valid_row(row):
    return len(row) >= 2 and row[0] != '' and row[1] != ''


def parse_sheet_data_row(row):
    name, email, *availabilities = row
    week_availability = parse_availabilities(availabilities)
    return {
        'name': name,
        'email': email,
        'availabilities': week_availability,
    }


def parse_availabilities(availabilities):
    return {
        day: [] if availability == '' else availability.split(',')
        for day, availability in zip(WEEKDAYS, availabilities)
    }
