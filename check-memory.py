#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os, fileinput, getpass, shutil, sys

def update_memory( input_file, temp_file, check):
    first = 1
    if check != 0:
        print "enable check memory"
    else:
        print "disable check memory"
    search1 = "kernel vmlinuz"
    search2 = "append ro initrd"
    search3 = "linux memtest86+.bin"
    found = 0
    foundmemory = 0
    with open(temp_file, "w") as text_file:
        for line in fileinput.input(input_file):
            #Αν θέλουμε έλεγχο μνήμης πρέπει να μπει σε σχόλια το search1
            if line[0:len(search1)] == search1:
                if check == 1:
                    if first == 1:
                        line = "#" + line
                        print line
                    found = 1
            #Αν θέλουμε έλεγχο μνήμης πρέπει να μπει σε σχόλια το search2
            if line[0:len(search2)] == search2:
                if check == 1:
                    if first == 1:
                        line = "#" + line
                        print line
                        print "foundmemory"
                        print foundmemory
                        #Αν δεν βρήκε μέχρι στιγμή το memetest το προσθέτει
                        if foundmemory == 0:
                            text_file.write( "linux memtest86+.bin\n")
                    found = 1
                first = 0
            #Αν δεν θέλουμε έλεγχο μνήμης πρέπει το search3 (memtest) να μπει από σχόλια
            if line[0:len(search3)] == search3:
                if check == 0:
                    if first == 1:
                        line = "#" + line
                    found = 1                
                    foundmemory = 1
            #Αν δεν θέλουμε έλεγχο μνήμης και βρει σε σχόλια το search1 τότε βγάζει τα σχόλια
            if line[1:len(search1)+1] == search1:
                if check == 0:
                    if first == 1:
                        line = line[1:]
                    found = 1
            #Αν δεν θέλουμε έλεγχο μνήμης και βρει σε σχόλια το search2 τότε βγάζει τα σχόλια
            #Αν θέλουμε έλεγχο μνήμης και δεν βρήκε τη γραμμή memtest τότε την προσθέτει στο αρχείο
            if line[1:len(search2)+1] == search2:
                if check == 0:
                    line = line[1:]
                    found = 1                    
                first = 0
            #Αν θέλουμε έλεγχο μνήμης πρέπει να βγάλουμε τα σχόλια από το search3 (memtest)
            if line[1:len(search3)+1] == search3:
                if check == 1:
                    if first == 1:
                        line = line[1:]
                    found = 1
                    foundmemory = 0
            text_file.write( line)
    if found == 0:
        print "ΔΕΝ χρειάστηκε αλλαγή"
    else:
        print "Έγινε η αλλαγή"
    return found


check = 0
if len( sys.argv) == 2:
    check = 1
input_file = "/var/lib/tftpboot/ltsp/i386/pxelinux.cfg/default"
temp_file = input_file + ".tmp"
bak_file = input_file + ".bak"
if update_memory( input_file, temp_file, check) != 0:
    shutil.copyfile( input_file, bak_file)
    shutil.copyfile( temp_file, input_file)


