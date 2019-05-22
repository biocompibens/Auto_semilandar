from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Imports from Toni inbox login
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import quopri
import email
from bs4 import BeautifulSoup

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
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/gmail.readonly']


# Function to login
def login():
    print('Logging in...')
    creds_calendar = None
    creds_inbox = None

    #store_inbox = file.Storage('token_inbox.json')
    #creds_inbox = store_inbox.get()

    #store = file.Storage('token.json')
    #creds = store.get()
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_calendar.pickle'):
        with open('token_calendar.pickle', 'rb') as token_calendar:
            creds_calendar = pickle.load(token_calendar)

    if os.path.exists('token_inbox.pickle'):
        with open('token_inbox.pickle', 'rb') as token_inbox:
            creds_inbox = pickle.load(token_inbox)


    # If there are no (valid) credentials for INBOX available, let the user log in.
    if not creds_inbox or not creds_inbox.valid:
        print ('\n\nCreating new credentials for inbox, check your browser!')

        #flow_inbox = client.flow_from_clientsecrets('credentials_inbox.json', SCOPES[1])
        #creds_inbox = tools.run_flow(flow_inbox, store_inbox)

        flow_inbox = InstalledAppFlow.from_client_secrets_file('credentials_inbox.json', SCOPES[1])
        creds_inbox = flow_inbox.run_local_server()

        with open('token_inbox.pickle', 'wb') as token_inbox:
            pickle.dump(creds_inbox, token_inbox)

        print ('[Done]')


    # If there are no (valid) credentials for CALENDAR available, let the user log in.
    if not creds_calendar or not creds_calendar.valid:
        print ('\n\nCreating new credentials for calendar, check your browser!')
        flow_calendar = InstalledAppFlow.from_client_secrets_file('credentials_calendar.json', SCOPES[0])
        creds_calendar = flow_calendar.run_local_server()
        print ('[Done]')


        # Save the credentials for the next run
        with open('token_calendar.pickle', 'wb') as token_calendar:
            pickle.dump(creds_calendar, token_calendar)


    service_calendar = build('calendar', 'v3', credentials=creds_calendar)
    #service_inbox = build('gmail', 'v1', http=creds_inbox.authorize(Http()))
    service_inbox = build('gmail', 'v1', credentials=creds_calendar)

    print ('[All done !]')
    return service_calendar, service_inbox

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

    # Creates the event
    new_event = service.events().insert(calendarId=calendar_id, body=event_dict).execute()

    # Prints a small log
    print ('\n{} | New event created:'.format(datetime.date.today()))
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
    service_calendar, service_inbox = login()
    create_new_event(service_calendar, test_event, calendar_id=team_calendar)
