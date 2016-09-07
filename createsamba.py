#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os, fileinput, getpass, shutil, sys

def update_samba( input_file, temp_file, name, dirname):
    search = "[" + name + "]"
    found = 0
    for line in fileinput.input(input_file):
        if line[0:len(search)] == search:
            found = 1
    if found == 0:
        with open(temp_file, "w") as text_file:
            for line in fileinput.input(input_file):
                text_file.write( line)
            text_file.write( "\n")
            text_file.write( search + "\n")
            text_file.write( "\tpath=" + dirname + "\n")
            text_file.write( "\twriteable = yes\n")
            text_file.write( "\tbrowsable = yes\n")
            text_file.write( "\tguest ok = yes\n")
        print "Έγινε η αλλαγή"
        return 1
    print "Καμία αλλαγή"
    return 0


def repair_samba( name, dirname):
    input_file = "/etc/samba/smb.conf"
    temp_file = input_file + ".tmp"
    bak_file = input_file + ".bak"
    if update_samba( input_file, temp_file, name, dirname) != 0:
        shutil.copyfile( input_file, bak_file)
        shutil.copyfile( temp_file, input_file)

dirname = os.environ['HOME'] + "/public";
try:
    os.stat(dirname)
except:
    os.mkdir(dirname)

repair_samba( "public", dirname)
