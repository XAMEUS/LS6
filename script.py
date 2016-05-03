import operator
import datetime
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
    t = [p[0] for p in sorted(d.items(), key=operator.itemgetter(1), reverse=True)][:n]
    for e in t:
        print(e)

def cote_moy_spam(path):
    mb = Mailbox(path)
    i = 0
    s = 0
    for m in mb:
        s += float(m.mail.get("X-Spam-Score"))
        i += 1
    print(s / i)

def msg_par_jour(path):
    mb = Mailbox(path)
    t = [0, 0, 0, 0, 0, 0, 0]
    for m in mb:
        d = datetime.datetime(m.Date[0], m.Date[1], m.Date[2], m.Date[3], m.Date[4], m.Date[5])
        t[d.weekday()] += 1
    print("lundi: " + str(t[0]))
    print("mardi: " + str(t[1]))
    print("mercredi: " + str(t[2]))
    print("jeudi: " + str(t[3]))
    print("vendredi: " + str(t[4]))
    print("samedi: " + str(t[5]))
    print("dimanche: " + str(t[6]))


if __name__ == "__main__":
    pays_plus_frequents("Messages", 5)
    cote_moy_spam("Messages")
    msg_par_jour("Messages")
