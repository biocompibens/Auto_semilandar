from bin.readEmail import GmailAPI


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


def EEB(message):
    """"""


def hugues(message):
    """"""
