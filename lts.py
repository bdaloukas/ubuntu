#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os, fileinput, getpass, shutil, sys

#Πρέπει να διαβάσω μία μία τις γραμμές και να προσέξω όσες έχουν το HOSTNAME,LDM_USERNAME,LDM_PASSWORD

def repair(line, username, tmima):
    if line[1:1] == "#":
        return line
    pos = line.find( "=")
    if pos == -1:
        return line
    token1 = line[0:pos]
    token2 = line[pos+1:].strip()
    if (token1 != "HOSTNAME") and (token1 != "LDM_USERNAME") and (token1 != "LDM_PASSWORD"):
        return line
    if len(token2) == 5:
        return token1+"="+token2+tmima+"\n"
    if len(token2) == 7:
        return token1+"="+token2[0:5]+tmima+"\n"
    return line

def change_tmima_do( input_file, temp_file, tmima):
    username = getpass.getuser()
    with open(temp_file, "w") as text_file:
        for line in fileinput.input(input_file):
            line = repair( line, username, tmima)
            text_file.write( line)

def change_tmima( tmima):
    input_file = '/var/lib/tftpboot/ltsp/i386/lts.conf'
    temp_file = '/var/lib/tftpboot/ltsp/i386/lts.conf.tmp'
    bak_file = '/var/lib/tftpboot/ltsp/i386/lts.conf.bak'
    shutil.copyfile( input_file, bak_file)
    change_tmima_do( input_file, temp_file, tmima)
    shutil.copyfile( temp_file, input_file)

tmima = ""
if len( sys.argv) == 2:
    tmima = str(sys.argv[1])
    if tmima == "xo":
        tmima = ""

if tmima != "":
    if len(tmima) == 2:
        print "Αλλαγή στο τμήμα " + tmima
        change_tmima( tmima)
if tmima == "":
    print "Αλλαγή σε ΧΩΡΙΣ ΤΜΗΜΑ"
    change_tmima( "")

