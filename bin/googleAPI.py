from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


class GoogleAPI(object):

    def __init__(self, credentials='credentials.json'):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials, SCOPES)
            creds = tools.run_flow(flow, store)

        self.gmail = build('gmail', 'v1', http=creds.authorize(Http()))
        self.calendar = build('calendar', 'v3', http=creds.authorize(Http()))
