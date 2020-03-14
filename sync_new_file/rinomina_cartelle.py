#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from_path = './origine/'
to_path = './destinazione/' 
real_origin = {}

remove = ' (Copia di backup collegamento simbolico)'
simulation = True

data = {}
import pdb; pdb.set_trace()
for mode, path in [('from', from_path), ('to', to_path)]:
    data[mode] = set()
    for root, folders, files in os.walk(path):
        clean_root = root.replace(remove, '')[len(path):]
        for filename in files:
            fullname = os.path.join(clean_root, filename)
            data[mode].add(fullname)
            
            if mode == 'from' and remove in root:
                real_origin[fullname] = \
                    os.path.join(root, filename)[len(path):]
                

new_data = data['from'] - data['to']

import pdb; pdb.set_trace()
for filename in new_data:
    origin = os.path.join(
        from_path, 
        real_origin.get(filename, filename),
        )

    destination = os.path.join(to_path, filename)
    
    if simulation:
        print origin, '>>', destination
    else:    
        os.copy(origin, destination)

