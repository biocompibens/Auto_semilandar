
## author: Auguste

import smtplib
import time
import imaplib
import email



ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "biocompibens" + ORG_EMAIL
FROM_PWD    = "pslmemolife"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('biocompibens@gmail.com','pslmemolife')
mail.list()
mail.select("inbox") # connect to inbox.

result, data = mail.uid('search', None, "ALL") # search and return uids instead
#latest_email_uid = data[0].split()[-1]

for i in data[0].split():
    result, data2 = mail.uid('fetch', i, '(RFC822)')
    raw_email = data2[0][1]
    msg = email.message_from_string(raw_email.decode('iso-8859-1'))
    #print(i)
    if 'ENS-AllBio' in msg['Subject']:
        #print(msg['Subject'])
        if msg.is_multipart():
            for part in msg.get_payload():
                print(part)
        else:
            print(msg.get_payload())




