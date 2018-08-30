#!/usr/bin/python;

import sys
import subprocess
import os
import hashlib

FIND_CMD = "find . -name \*.* -print"
BUFFER = 65536

#Get path from the user
root_path = sys.argv[1]
#Checks that the user sent path
if not root_path:
 print("Error: No file specified.Please try again ")
 sys.exit(1)
#Chage working path
os.chdir(root_path)
#Get all the possible paths under the given directory
dirty_out = subprocess.run(FIND_CMD.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
file_list = dirty_out.stdout.decode("utf-8").splitlines()
#Find files with the same size and add to dic
same_size = dict()
for file in file_list:
   path = root_path + file[1:]
   if os.path.isdir(path):
        continue
   if os.path.exists(path):
        file_size = os.path.getsize(path)
        #Add the path to dictionary by size
        if file_size not in same_size:
         same_size[file_size] = list([path])
        else:
         same_size[file_size].append(path)

#print same size dict for testing
"""for size in same_size:
    if len(same_size[size]) > 1:
        print("{0}\n".format(",".join(same_size[size])))
"""
#Find files with the same size and hash code
file_signatures = dict()
for size in same_size:
 if len (same_size[size]) > 1:
    i = 0
    while i < len (same_size[size]):
     # Hash file content with read buffer
     md5 = hashlib.md5()
     path = same_size[size][i]
     md5 = hashlib.md5()
     with open(path, 'rb') as f:
            while True:
                data = f.read(BUFFER)
                if not data:
                    break
                md5.update(data)
            md5_sig = md5.hexdigest()
            # Add to dictionary only files with the same size and hash
            if md5_sig not in file_signatures:
                file_signatures[md5_sig] = list([path])
            else:
                file_signatures[md5_sig].append(path)
     i=i+1
#Prints the path of all the duplicate files separated with , 
for sig in file_signatures:
    if len(file_signatures[sig]) > 1:
        print("{0}\n".format(",".join(file_signatures[sig])))







