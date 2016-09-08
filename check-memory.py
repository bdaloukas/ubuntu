#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os, fileinput, getpass, shutil, sys

def update_memory( input_file, temp_file, check):
    if check != 0:
        print "enable check memory"
    else:
        print "disable check memory"
    search1 = "kernel vmlinuz"
    search2 = "append ro initrd"
    found = 0
    with open(temp_file, "w") as text_file:
        for line in fileinput.input(input_file):
            if line[0:len(search1)] == search1:
                if check == 0:
                    line = "#" + line
                    found = 1
            if line[0:len(search2)] == search2:
                if check == 0:
                    line = "#" + line
                    found = 1
            if line[1:len(search1)+1] == search1:
                if check == 1:
                    line = line[1:]
                    found = 1
            if line[1:len(search2)+1] == search2:
                if check == 1:
                    line = line[1:]
                    found = 1                    
            text_file.write( line)
    if found == 0:
        print "ΔΕΝ χρειάστηκε αλλαγή"
    else:
        print "Έγινε η αλλαγή"
    return found


check = 0
if len( sys.argv) == 2:
    check = 1
input_file = "PXELinux"
temp_file = input_file + ".tmp"
bak_file = input_file + ".bak"
if update_memory( input_file, temp_file, check) != 0:
    shutil.copyfile( input_file, bak_file)
    shutil.copyfile( temp_file, input_file)


