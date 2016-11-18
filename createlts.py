#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os

def scan_network():
    #s = os.system("arp -a > a.txt")
    f = open('a.txt', "r")
    for line in f:
        pos = line.find( ".local")
        if pos == -1:
            continue
        pos = line.find( " ")
        if pos == -1:
            continue
        computer = line[ 0:pos]
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
        mac = line2[ 0:pos]
        print "computer=" + computer + "  mac=" + mac
        UpdateLTS( mac, computer)
        
def UpdateLTS(mac, computer)
    filename = "/var/lib/tftboot/lts/i386/lts.conf"
        with open(filename, "r") as text_file:    
            #text_file.write( "#!/bin/sh\n")
    
ret = scan_network()
#print ret
