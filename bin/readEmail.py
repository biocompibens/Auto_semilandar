import base64
from bs4 import BeautifulSoup

from bin.googleAPI import GoogleAPI

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

    for message in messages:
        if "parts" in message:  # multipart email (rare)
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

        content = base64.urlsafe_b64decode(message['body']['data'])

        if mime == 'text/html':
            content = BeautifulSoup(content.decode('utf-8'),
                                    'html.parser').text
        return content

if __name__ == '__main__':
    main()
