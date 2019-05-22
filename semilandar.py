from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from IPython import embed
import numpy as np

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
    'dateTime': '2019-05-22T19:00:00',
    'timeZone': 'Europe/Paris',
  }
  }

test_event2 = {
  'colorId' : '2',
  'summary': 'Hackathon test event',
  'location': '45 rue dUlm',
  'description': 'Is it going to work ?',
  'start': {
    'dateTime': '2019-05-22T14:00:00',
    'timeZone': 'Europe/Paris',
  },
  'end': {
    'dateTime': '2019-05-22T20:00:00',
    'timeZone': 'Europe/Paris',
  }
  }

# Update some fields
test_event=['start']['timeZone']='Europe/Paris'
test_event=['end']['timeZone']='Europe/Paris'



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
def check_reminder(event, service):
    import Levenshtein
    # use pip install python-Levenshtein
    events_result = service.events().list(calendarId=team_calendar, timeMin= datetime.datetime.utcnow().isoformat() + 'Z' , singleEvents=True,
                                        orderBy='startTime').execute()#'p6o50l43pqssqamaip3kdb3k4g@group.calendar.google.com'# 'Z' indicates UTC time

    for ev in events_result['items']:
        #print( ev['summary'])
        #embed()
        lenMinSeq = np.min([len(event['summary']),len(ev['summary'])])
        strDist = Levenshtein.distance(unicode(event['summary'], 'utf-8').lower(), ev['summary'].lower())
        pourcentageSimilarities = strDist/1 #float(lenMinSeq)
        if pourcentageSimilarities <= 5 :
            print("event already present")
            print( ev['summary'])
            embed()
            flagLoc = 0
            flagDate = 0
            flagTimeStart = 0
            locDist = Levenshtein.distance(str(event['location']), str(ev['location']))
            locPourcentageSimilarities = 100 * locDist/float(len(event['location']))
            if locPourcentageSimilarities <= 80. :
                print("location change from : " +ev['location'] + " to : " +event['location'])
                #ev['location'] = event['location'] 
                flagLoc = 1
            dateDist = Levenshtein.distance(str(event['start']['dateTime']), str(ev['start']['dateTime']))
            if dateDist != 0 :
                print("start dateTime change from : " +ev['start']['dateTime'] + " to : " +event['start']['dateTime'])
                #ev['start']['dateTime'] = event['start']['dateTime']

                flagDate = 1
                startEvent = datetime.datetime.fromisoformat(event['start']['dateTime'])
                start_dateEvent = startEvent.strftime("%Y-%m-%d")
                start_timeEvent = startEvent.strftime("%H:%M:%S")


                startEv = datetime.datetime.fromisoformat(ev['start']['dateTime'])
                start_dateEv = startEv.strftime("%Y-%m-%d")
                start_timeEv = startEv.strftime("%H:%M:%S")

                endEv = datetime.datetime.fromisoformat(ev['end']['dateTime'])
                end_dateEv = endEv.strftime("%Y-%m-%d")
                end_timeEv = endEv.strftime("%H:%M:%S")

                formatTime = '%H:%M:%S'
                evDuration = datetime.strptime(end_timeEv, formatTime) - datetime.strptime(start_timeEv, formatTime)
                evDurationH = datetime.strftime(evDuration ,'%H')
                evDurationM = datetime.strftime(evDuration ,'%M')




                print("end dateTime change")
                event['end']['dateTime'] = event['start']['dateTime'] + datetime.detlatime(minutes= evDurationM,hours = evDurationH )
                event['end']['timeZone'] = 'Europe/Paris'
            service.events().update(calendarId=team_calendar,eventId = ev['id'], body = event).execute()
            return 1

    return 0
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
    check_reminder(test_event2, service_calendar) #1 if a reminder else 0
