import operator
from Message import Message
from Mailbox import Mailbox

def pays_plus_frequents(path, n):
    mb = Mailbox(path)
    d = {}
    for m in mb:
        pays = m.From.split("@")[1].split(".")[-1]
        if not pays in d:
            d[pays] = 1
        else:
            d[pays] += 1
    return [p[0] for p in sorted(d.items(), key=operator.itemgetter(1), reverse=True)][:n]

def cote_moy_spam(path):
    mb = Mailbox(path)
    i = 0
    s = 0
    for m in mb:
        s += float(m.mail.get("X-Spam-Score"))
        i += 1
    return s / i

def msg_par_jour(path):
    mb = Mailbox(path)
    return 0

if __name__ == "__main__":
    print(pays_plus_frequents("Messages", 5))
    print(cote_moy_spam("Messages"))
