import re

from bin.readEmail import create_list_dictionary


class Template(object):

    def __init__(self, message):
        """message = dict with keys 'body' 'subject' 'to' 'from' 'date' """
        if message.get('from') == "virginie.bues@ens.fr":
            self.render = virginie_template


def virginie_template(message):
    """"""


def neurosection(message):
    """"""


def colot(message):
    """"""


def Developmental(message):
    """"""


def bioinfo_seminar(message):
    """"""
    info = {}
    content = message['Body']
    info['creator'] = message['From']
    date = re.search(r"\w+\s(\d{1,2}\s\w+)\sat\s(\d{1,2}\w{2})", content)
    if date:
        date = date.group(1) + " " + date.group(2)
        print(date)

    where = re.search(r"\sin\s(.+)\sat(.+\(.+\))", content)
    if where:
        where = where.group(1) + " " + where.group(2)
        print(where)

    talker = re.search(r",\s(.+?)\swill", content)

    if talker:
        talker = talker.group(1)
        if "," in talker:
            talker = talker.split(",")[-1]
        print(talker)

def EEB(message):
    """"""


def hugues(message):
    """"""


def main():
    mails = create_list_dictionary()
    msg = [m for m in mails if 'Next Bioinfo' in m["Subject"]][0]
    # for msg in mails:
    bioinfo_seminar(msg)
    # print(msg)


if __name__ == '__main__':
    main()