import email;
import re;


class Message:

    def __init__(self,fname):
        self.name = fname
        self.Received = []
        f = open(fname,"r")
        text = f.read()
        self.mail = email.message_from_string(text)
        self.From = email.utils.parseaddr(self.mail.get("From"))[1]

        self.To = email.utils.parseaddr(self.mail.get("To"))[1]
        self.Date = email.utils.parsedate(self.mail.get("Date"))
        self.Subject = self.mail.get("Subject")
        for i in self.mail.get_all("Received"):
            m = re.search(r"by ([^( )]*) \(",i)
            m2 = re.search(r"; (.*)",i)
            if(m != None and m2!= None):
                self.Received.append((m.group(1),m2.group(1)))

    def __str__(self):
        s = "Received: "
        for i in self.Received[::-1]:
            s+=">>> "+i[0]+" "+i[1]+"\n"
        return "From: "+str(self.From)+"\nTo: "+str(self.To)+"\nDate: "+str(self.Date)+"\nSubject: "+str(self.Subject)+"\n"+s

if __name__ == "__main__" :
    m = Message("Messages/183000.emlx")
    print(m)
