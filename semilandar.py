from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        print (calendar_list.keys())
        for calendar_list_entry in calendar_list['items']:

            print (calendar_list_entry['summary'])
            print (calendar_list_entry['id'])
            print ('\n')

            page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='p6o50l43pqssqamaip3kdb3k4g@group.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    # Adding a new events
    print ('\nAdding new event...')
    our_id = 'p6o50l43pqssqamaip3kdb3k4g@group.calendar.google.com'
    event = {
      'colorId' : '2',
      'summary': 'HACKATHON CONTINUES',
      'location': '46 rue dUlm',
      'description': 'Is it going to work ?',
      'start': {
        'dateTime': '2019-05-22T09:00:00',
        'timeZone': 'Europe/Paris',
      },
      'end': {
        'dateTime': '2019-05-22T18:00:00',
        'timeZone': 'Europe/Paris',
      }
      }
    new_event = service.events().insert(calendarId=our_id, body=event).execute()
    print ('Event created')


if __name__ == '__main__':
    main()

#### Start of the final real script

# Function to login
def login():
    return None
#End login

# Function process event
def process_event():
    return None
# End process event

# Function to check reminder
def check_reminder():
    return None
# End check reminder

# Function to create a new event
def create_new_event():
    return None
# End create new event

# Function update event
def update_event():
    return None
# End update event
