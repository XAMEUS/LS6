import email;
import re;


class Message:

    def __init__(self,fname):
        self.name = fname
        self.Received = []
        f = open(fname,"r")
        text = f.read()
        self.mail = email.message_from_string(text)
        self.From = self.mail.get("From")
        if(self.From != None):
            m = re.search(r"<([^>]*)>",self.From)
            if(m != None):
                self.From = m.group(1)
            else:
                self.From = None
        self.To = self.mail.get("To")
        if(self.To != None):
            m = re.search(r"<([^>]*)>",self.To)
            if(m != None):
                self.To = m.group(1)
            else:
                self.To = None
        self.Date = self.mail.get("Date")
        self.Subject = self.mail.get("Subject")
        for i in self.mail.get_all("Received"):
            m = re.search(r"by ([^( )]*) \(",i)
            m2 = re.search(r"; (.*)",i)
            if(m != None and m2!= None):
                self.Received.append((m.group(1),m2.group(1)))

    def __str__(self):
        s = ""
        return "From: "+str(self.From)+"\nTo: "+str(self.To)+"\nDate: "+str(self.Date)+"\nSubject: "+str(self.Subject)+"\n"

if __name__ == "__main__" :
    m = Message("Messages/183000.emlx")
    print(m)
