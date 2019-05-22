
## author: Auguste

import smtplib
import time
import imaplib
import email
import sys
from bs4 import BeautifulSoup


ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "biocompibens" + ORG_EMAIL
FROM_PWD    = "pslmemolife"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('biocompibens@gmail.com','pslmemolife')
mail.list()
mail.select("inbox") # connect to inbox.

good_formats = ["text/plain", "text/html"]

result, data = mail.uid('search', None, "ALL") # search and return uids instead
#latest_email_uid = data[0].split()[-1]
contents = []

for i in data[0].split():
    result, data2 = mail.uid('fetch', i, '(RFC822)')
    raw_email = data2[0][1]
    msg = email.message_from_string(raw_email.decode('iso-8859-1'))
    print(i, end=", ")
    if 'ENS-AllBio' in msg['Subject']:
        if msg.is_multipart():
            contents.append('')
            for part in msg.get_payload():
                print(part.get_content_type())
                if part.get_content_type() == "text/plain":
                    contents[-1] += part.get_payload()
                elif part.get_content_type() == "text/html":
                    contents[-1] += BeautifulSoup(part.get_payload()).text
        else:
            if msg.get_content_type() == "text/plain":
                contents.append(msg.get_payload())
            elif msg.get_content_type() == "text/html":
                contents.append(BeautifulSoup(msg.get_payload()).text)
        if i == 5:
            sys.exit(0)





