#!/usr/bin/env python3

import sys
import os
from Mailbox import Mailbox
import shutil


m = Mailbox(sys.argv[1])

if not os.path.isdir(sys.argv[2]):
    os.makedirs(sys.argv[2])

listPays = []

for msg in m :
    pays = msg.From.split("@")[1].split(".")[-1]
    if pays not in listPays:
        listPays.append(pays)
    if not os.path.isdir(sys.argv[2]+"/"+pays):
        os.mkdir(sys.argv[2]+"/"+pays)
    shutil.copyfile(msg.path,sys.argv[2]+"/"+pays+"/"+msg.name)

for pays in listPays:
    os.system("tar -czvf "+sys.argv[2]+"/"+pays+".tgz "+sys.argv[2]+"/"+pays)
    shutil.rmtree(sys.argv[2]+"/"+pays)
