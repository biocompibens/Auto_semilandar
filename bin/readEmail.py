from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import quopri
import email

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")

    else:
        print("Message snippets:")
        for message in messages[:1]:
            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()

            # base 62 renvoie un string encodé, mais la fonction par défaut de python ne peut pas le décoder...
            msg_str = base64.urlsafe_b64decode(msg['raw'])

            mime_msg = email.message_from_string(msg_str.decode())

            print(mime_msg)
           # for part in msg['payload']['parts']:
            #    print(part['body'])



if __name__ == '__main__':
    main()
