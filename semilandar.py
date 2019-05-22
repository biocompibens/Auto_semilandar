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
    print('Logging in...')
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print ('- Creating new credentials, check your browser!')
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
    print ('[Done]')
    return service

#End login

# Function process event
def process_event():
    return None
# End process event

# Function to check reminder
def check_reminder(event, service):
    import Levenshtein
    # use pip install python-Levenshtein
    events_result = service.events().list(calendarId=team_calendar, timeMin=now, singleEvents=True,
                                        orderBy='startTime').execute()#'p6o50l43pqssqamaip3kdb3k4g@group.calendar.google.com'
	for ev in events_results:
    	strDist = Levenshtein.distance(event['summary'], ev['summary'])
		pourcentageSimilarities = 100 *strDist/float(len(event['summary']))
		if pourcentageSimilarities >= 80. :
			flagLoc = 0
			flagDate = 0
			flagTimeStart = 0
			locDist = Levenshtein.distance(event['location'], ev['location'])
			locPourcentageSimilarities = 100 * locDist/float(len(event['location']))
			if locPourcentageSimilarities <= 80. :
				print("location change from : " +ev['location'] + " to : " +event['location'])
				#ev['location'] = event['location'] 
				flagLoc = 1
			dateDist = Levenshtein.distance(event['dateTime'], ev['locationTime'])
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
    service = login()
    create_new_event(service, test_event, calendar_id=team_calendar)
