#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os, shutil

def scan_network():
    s = os.system("arp -a > a.txt")
    f = open('a.txt', "r")
    for line in f:
        pos = line.find( ".local")
        if pos == -1:
            continue
        computer = line[ 0:pos]
        if computer[ 0:4] != "ltsp":
            continue
        pos = line.find( ')')
        if pos == -1:
            continue
        line2 = line[ pos+1:]
        pos = line2.find( ' ')
        line2 = line2[ pos+1:]
        pos = line2.find( ' ')
        if pos == -1:
            continue
        line2 = line2[ pos+1:]
        pos = line2.find( ' ')
        if pos == -1:
            continue
        mac = line2[ 0:pos].upper()
        UpdateLTS( mac, computer)
        
def ComputeUserName( computer):
    s = os.system("who > b.txt") 
    f = open('b.txt', "r")
    search = "(" + computer + ".local)"    
    for line in f:
        if line.find( search) == -1:
            continue
        pos = line.find( " ")
        if pos == -1:
            continue
        username = line[ 0:pos]
        return username
                
def UpdateLTS(mac, computer):
    print "computer=" + computer + "  mac=" + mac
    filename = "/var/lib/tftpboot/ltsp/i386/lts.conf"
    temp_file = filename + ".tmp"
    search = "[" + mac + "]"
    lensearch = len( search)
    with open(filename, "r") as input_file:
        for line in input_file:
            #print "search=" + search + " l=" + line[ 0:lensearch]
            if line[ 0:lensearch] == search:
                return
            #text_file.write( "#!/bin/sh\n")
    print "must change"
    username = ComputeUserName( computer)
    with open(filename, "r") as input_file:
        with open(temp_file, "w") as text_file:
            for line in input_file:
                text_file.write( line)
            text_file.write( search + "\n")
            text_file.write( "HOSTNAME=" + username + "\n")
            text_file.write( "LDM_USERNAME=" + username + "\n")
            text_file.write( "LDM_PASSWORD=" + username + "\n")
            text_file.write( "LDM_AUTOLOGIN=True\n")
            text_file.write( "\n")

    bak_file = filename + ".bak"
    shutil.copyfile( filename, bak_file)
    shutil.copyfile( temp_file, filename)
                     
scan_network()
#print ret


