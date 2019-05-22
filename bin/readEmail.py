from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import quopri
import email
from bs4 import BeautifulSoup

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

        for message in messages[:5]:
            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()

            # base 62 renvoie un string encodé, mais la fonction par défaut de python ne peut pas le décoder...
            msg_str = base64.urlsafe_b64decode(msg['raw'])

            mime_msg = email.message_from_string(msg_str.decode('iso-8859-1'))


            for parts in mime_msg.walk():
                mime_msg.get_payload()
                print(parts.get_content_type())
                if parts.get_content_type() == 'text/plain':
                    myMSG=base64.urlsafe_b64decode(parts.get_payload().encode('utf-8')).decode()
                    print(myMSG)
                if parts.get_content_type() == 'text/html':
                    try:
                        myMSG_html=base64.urlsafe_b64decode(parts.get_payload().encode('utf-8')).decode()
                        myMSG = BeautifulSoup(myMSG_html, 'html.parser').text
                    except:
                        myMSG = BeautifulSoup(parts.get_payload().encode('iso-8859-1'), 'html.parser').text

                    print(myMSG)


            # if mime_msg.is_multipart():
            #     part = mime_msg.get_payload()[0]
            #     char_set = part['Content-Type'].split('charset=')[-1].split(';')[0].strip('"').lower()
            # else:
            #     char_set = mime_msg['Content-Type'].split('charset=')[-1].split(';')[0].strip('"').lower()
            #
            # if mime_msg.is_multipart():
            #     body = mime_msg.get_payload()[0].get_payload()
            # else:
            #     body = mime_msg.get_payload()
            #
            # print(body)
            # print(char_set)
            #
            # if char_set.lower() != 'iso-8859-1':
            #     mime_msg = email.message_from_string(msg_str.decode(char_set))
            #
            # if mime_msg.is_multipart():
            #     body = mime_msg.get_payload()[0].get_payload()
            # else:
            #     body = mime_msg.get_payload()
            #
            # print(body)
            #

           # for part in msg['payload']['parts']:
            #    print(part['body'])



if __name__ == '__main__':
    main()
