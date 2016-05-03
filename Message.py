class Message:

    def __init__(self,fname):
        self.name = fname
        self.From = ""
        f = open(fname,"r")
        lines = f.readlines()
        for l in lines:
            if l.startswith("From:"):
                self.From = self.getData(l)
            elif l.startswith("To:"):
                self.To = self.getData(l)
            elif l.startswith("Date:"):
                self.Date = self.getData(l)
            elif l.startswith("Subject:"):
                self.Subject = self.getData(l)

    def __str__(self):
        return "From: "+self.From+"\nTo: "+self.To+"\nDate: "+self.Date+"\nSubject: "+self.Subject+"\n"
    
    def getData(s):
        return s.split(":")[1].strip()
