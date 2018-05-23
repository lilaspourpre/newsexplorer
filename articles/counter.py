# -*- coding: UTF-8 -*-
import os
import codecs
path = "Documents/RUtexts"
files = os.listdir(path)
path = path.replace("/", "\\")
path1 = os.path.abspath(__file__).replace("counter.py", "")
count = 0
errors = 0
mytxt = filter(lambda x: x.endswith('.txt'), files)
for i in mytxt:
    try:
        text = codecs.open(path1+path+"\\"+i, 'r', 'utf-8').read()
        if u"Путин" in text:
            print i.decode("cp1251")
            count += 1
    except:
        errors += 1
        pass
print count