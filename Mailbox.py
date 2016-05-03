import os
from Message import Message

def load(path):
    l = []
    for dirs, sdirs, files in os.walk(path):
        for fname in files:
            l.append(os.path.join(dirs, fname))
    return l

class Mailbox:
    def __init__(self, path):
        self.msg_list = []
        for msg in load(path):
            self.msg_list.append(Message(msg))

if __name__ == "__main__":
    mb = Mailbox("Messages")
    print(mb.msg_list)
    for msg in mb.msg_list:
        print(msg)
