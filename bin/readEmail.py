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

        for message in messages[:2]:
            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()

            # base 62 renvoie un string encodé, mais la fonction par défaut de python ne peut pas le décoder...
            msg_str = base64.urlsafe_b64decode(msg['raw'])

            mime_msg = email.message_from_string(msg_str.decode('iso-8859-1'))
            if mime_msg.is_multipart():
                part = mime_msg.get_payload()[0]
                char_set = part['Content-Type'].split('; ')[-1].split('=')[-1]
            else:
                char_set = mime_msg['Content-Type'].split('; ')[-1].split('=')[-1]

            if mime_msg.is_multipart():
                body = mime_msg.get_payload()[0].get_payload()
            else:
                body = mime_msg.get_payload()

            print(body)

            if char_set.lower() != 'iso-8859-1':
                mime_msg = email.message_from_string(msg_str.decode(char_set))

            if mime_msg.is_multipart():
                body = mime_msg.get_payload()[0].get_payload()
            else:
                body = mime_msg.get_payload()

            print(body)


           # for part in msg['payload']['parts']:
            #    print(part['body'])



if __name__ == '__main__':
    main()
