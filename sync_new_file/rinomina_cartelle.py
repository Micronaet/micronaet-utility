#!/usr/bin/python
# -*- coding: utf-8 -*-

def check_if_is_unused_item(name):
    if '.dropbox' in name:
       return True
    if 'desktop.ini' in name:
       return True
    return False   
       
import os
from_path = '/root/Dropbak/Dropbox (Fiam Spa)/'
from_remove = len(from_path)

to_path = '/root/Dropbox (Fiam Spa)/' 
to_remove = len(to_path)

remove = ' (Copia di backup collegamento simbolico)'

simulation = True
data = {}
i = 0
for root, folders, files in os.walk(from_path):
    if check_if_is_unused_item(root):
        continue

    i += 1
    if i % 100 == 0:
       print('%s cartelle lette da origine' % i)
       
    origin_root = root[from_remove:]  # Remove start part
    clean_root = origin_root.replace(remove, '')
    for filename in files:
        if check_if_is_unused_item(filename):
            continue

        fullname = os.path.join(clean_root, filename)
        data[fullname] = os.path.join(origin_root, filename)

i = 0
removed = 0
for root, folders, files in os.walk(to_path):  
    if check_if_is_unused_item(root):
        continue
        
    i += 1
    if i % 100 == 0:
       print('%s cartelle lette da destinazione' % i)
    for filename in files:
        if check_if_is_unused_item(filename):
            continue

        clean_name = os.path.join(root, filename)[to_remove:]
        if clean_name in data:
            removed += 1
            del(data[clean_name])
            if removed % 50 == 0:
               print('%s rimossi da origine' % removed)               

out_f = open('output.csv', 'w')
i = 0
for clean_name in data:
    i += 1
    if i % 100 == 0:
       print('%s record written' % i)
       out_f.flush()

    origin = os.path.join(
        from_path,
        data[clean_name],
        )
    destination = os.path.join(to_path, clean_name)

    if os.path.isfile(destination):
        continue

    if simulation:
        #print origin, '>>', destination
        out_f.write('%s >> %s\n' % (origin, destination))
        
    else:
        os.copy(origin, destination)
out_f.close()
