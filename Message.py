import email;


class Message:

    def __init__(self,fname):
        self.name = fname
        f = open(fname,"r")
        text = f.read()
        self.mail = email.message_from_string(text)
        self.From = self.mail.get("From")
        self.To = self.mail.get("To")
        self.Date = self.mail.get("Date")
        self.Subject = self.mail.get("Subject")


    def __str__(self):
        return "From: "+self.From+"\nTo: "+self.To+"\nDate: "+self.Date+"\nSubject: "+self.Subject+"\n"
