from bin.readEmail import GmailAPI


class Template(object):

    def __init__(self, message):
        """message = dict with keys 'body' 'subject' 'to' 'from' 'date' """
        if message.get('from') == "virginie.bues@ens.fr":
            self.render = virginie_template


def virginie_template():
    """"""