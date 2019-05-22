import base64
import pickle

from bs4 import BeautifulSoup
from googleAPI import GoogleAPI

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

class GmailAPI(GoogleAPI):

    def get_all_messages_id(self):
        return [c["id"] for c in self.gmail.users().messages().list(
            userId='me'
        ).execute().get('messages', [])]


    def get_message_payload(self, id):
        return self.gmail.users().messages().get(
            userId='me', id=id, format="full"
        ).execute()['payload']



def main():
    gmail = GmailAPI()

    messages = [gmail.get_message_payload(i)
                for i in gmail.get_all_messages_id()]
    result = []
    for message in messages:
        if "parts" in message:  # multipart email (rare)
            header = message['headers']
            message = [c for c in message['parts'] if 'data' in c['body']]
            # get body from all part
            mimes = [c['mimeType'] for c in message]
            # get mimetype from all part
            try:
                message = message[mimes.index('text/plain')]
                mime = 'text/plain'
                # try to get body in plain text
            except (IndexError, ValueError):
                message = message[0]  # fallback to first if not
                mime = mimes[0]
        else:
            mime = message['mimeType']
            header = message['headers']

        content = base64.urlsafe_b64decode(message['body']['data'])

        if mime == 'text/html':
            content = BeautifulSoup(content.decode('utf-8'),
                                    'html.parser').text
        d = header_to_dict(header)
        if check_headers_complete(d):
            dico = mail_to_dict(d, content)
            # print(dico)
            result.append(dico)

    with open('mail_dict', 'wb') as out:
        pickle.dump(result, out)


def header_to_dict(header):
    res = {}
    for dic in header:
        res[dic['name']] = dic['value']
    return res


def check_headers_complete(dictio):
    return ('Date' in dictio.keys()) & ('Subject' in dictio.keys()) & ('To' in dictio.keys()) & (
            'From' in dictio.keys())


def mail_to_dict(header_dict, content):
    dico = {'From': header_dict['From'], 'To': header_dict['To'],
            'Date': header_dict['Date'], 'Subject': header_dict['Subject'],
            'Body': content}
    return dico


if __name__ == '__main__':
    main()
