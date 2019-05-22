from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def is_seminar(message_header):
    seminar_words = ['seminar', 'workshop', 'thesis', 'defense', 'talk', 'séminaire', 'séminaires', 'thèse',
                     'seminaire', 'seminaires', 'club', '']



def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(
        userId='me'
    ).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")

    else:

        for message in messages:
            msg = service.users().messages().get(userId='me',
                                                 id=message['id'],
                                                 format="full").execute()
            result = msg['payload']
            # print(msg['payload']['headers'])

            if "parts" in result:  # multipart email (rare)
                result = [c for c in result['parts'] if 'data' in c['body']]
                # get body from all part
                mimes = [c['mimeType'] for c in result]
                # get mimetype from all part
                try:
                    result = result[mimes.index('text/plain')]
                    mime = 'text/plain'
                    # try to get body in plain text
                except (IndexError, ValueError):
                    result = result[0]  # fallback to first if not
                    mime = mimes[0]
            else:
                mime = result['mimeType']

            content = base64.urlsafe_b64decode(result['body']['data'])

            if mime == 'text/html':
                content = BeautifulSoup(content.decode('utf-8'),
                                        'html.parser').text
            # print(content)

            d = header_to_dict(result)
            if check_headers_complete(d):
                dico = mail_to_dict(d, content)
                print(dico)

def header_to_dict(header):
    res = {}
    for dic in header['headers']:
        res[dic['name']] = dic['value']
    return res


def check_headers_complete(dictio):
    return ('Date' in dictio.keys()) & ('Subject' in dictio.keys()) & ('To' in dictio.keys()) & (
    'From' in dictio.keys())


def mail_to_dict(header_dict, content):
    dico = {'From': header_dict['From'], 'To': header_dict['Date'], 'Date': header_dict['Date'],
            'Subject': header_dict['Subject'], 'Body': content}
    return dico

if __name__ == '__main__':
    main()
