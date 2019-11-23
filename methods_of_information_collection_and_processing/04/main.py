import Parser
from pprint import pprint
if __name__ == "__main__":
    mail = Parser.MailNewsParser()
    lenta = Parser.LentaNewsParser()
    res = mail.parse_all() + lenta.parse_all()
    pprint(res)
