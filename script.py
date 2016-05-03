import operator
import datetime
import email
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

def duree_acheminement(path):
    m = Message(path)
    date0 = email.utils.parsedate_tz(m.Date)
    date1 = email.utils.parsedate_tz(m.Received[0][1])
    print(email.utils.mktime_tz(date1) - email.utils.mktime_tz(date0))

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
        date = email.utils.parsedate(m.Date)
        d = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5])
        t[d.weekday()] += 1
    print("lundi: " + str(t[0]))
    print("mardi: " + str(t[1]))
    print("mercredi: " + str(t[2]))
    print("jeudi: " + str(t[3]))
    print("vendredi: " + str(t[4]))
    print("samedi: " + str(t[5]))
    print("dimanche: " + str(t[6]))

if __name__ == "__main__":
    # pays_plus_frequents("Messages", 5)
    # cote_moy_spam("Messages")
    # msg_par_jour("Messages")
    duree_acheminement("Messages/msg.eml")
