from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# This is the ID for the calendar we need to add events_result
team_calendar = 'p6o50l43pqssqamaip3kdb3k4g@group.calendar.google.com'
# This is a test event, to help with development
test_event = {
  'colorId' : '2',
  'summary': 'Hackathon test event',
  'location': '46 rue dUlm',
  'description': 'Is it going to work ?',
  'start': {
    'dateTime': '2019-05-22T09:00:00',
    'timeZone': 'Europe/Paris',
  },
  'end': {
    'dateTime': '2019-05-22T11:00:00',
    'timeZone': 'Europe/Paris',
  }
  }

#TODO: update some fields

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']





# Function to login
def login():
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

    return service



#### Start of the final real script


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
def create_new_event(service, event_dict, calendar_id=team_calendar):
    # Check the dictionary
    if type(event_dict) is dict:
        pass
    else:
        print ('Problem, didnt receive a dictionary!')
        return

    print ('Creating new event...'),
    new_event = service.events().insert(calendarId=calendar_id, body=event_dict).execute()
    print ('[Done]')

    print ('\nNew event created:')
    print ('\t{}'.format(event_dict['summary']))
    print ('\t{}'.format(event_dict['location']))
    print ('\t{}'.format(event_dict['description']))
    print ('\tfrom {} to {}'.format(event_dict['start']['dateTime'],
    event_dict['end']['dateTime']))
    return None
# End create new event

# Function update event
def update_event():
    return None
# End update event


if __name__ == '__main__':
    service = login()
    create_new_event(service, test_event, calendar_id=team_calendar)
