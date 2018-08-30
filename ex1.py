#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import hashlib

BUFFER = 65536

# Get path from the user and check that user sent path

if len(sys.argv) >= 2:
    root_path = sys.argv[1]
else:
    sys.exit("Error: No path specified.Please try again ")

# Chage working path

if os.path.isdir(root_path):
    os.chdir(root_path)
else:
    sys.exit("Error: The path provided don't exsit. Please try again.")

# Get all the possible paths under the given directory

file_list = []
for root, _, filenames in os.walk(root_path):
     for filename in filenames:
         file_list.append(os.path.join(root, filename))

# Find files with the same size and add to dic

same_size = dict()
for file in file_list:
    path = '/' + file[1:]
    if not os.path.isdir(path) and os.path.exists(path):
        file_size = os.path.getsize(path)

        # Add the path to dictionary by size

        if file_size not in same_size:
            same_size[file_size] = list([path])
        else:
            same_size[file_size].append(path)

# Find files with the same size and hash code

file_signatures = dict()
for size in same_size:
    if len(same_size[size]) > 1:
        for i in range(len(same_size[size])):

     # Hash file content with read buffer

            md5 = hashlib.md5()
            path = same_size[size][i]
            with open(path, 'rb') as f:
                data = f.read(BUFFER)
                while data:
                    md5.update(data)
                    data = f.read(BUFFER)
                md5_sig = md5.hexdigest()

            # Add to dictionary only files with the same size and hash

                if md5_sig not in file_signatures:
                    file_signatures[md5_sig] = list([path])
                else:
                    file_signatures[md5_sig].append(path)

# Prints the path of all the duplicate files separated with ,

for sig in file_signatures:
    if len(file_signatures[sig]) > 1:
        print ("{0}\n".format(",".join(file_signatures[sig])))

