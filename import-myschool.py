#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2017 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import sys,crypt,pwd,grp,os

def dorun( cmd, run):
    if cmd == "" :
        return
    if run != 0 :
        print cmd
        os.system( cmd)
    if run == 0:
        print cmd
        
def createUser(name, username, password, users):
    if username in users:
        return ''
    encPass = crypt.crypt(password,"22")
    return "useradd -p "+encPass+ " -s "+ "/bin/bash "+ "-d "+ "/home/" + username+ " -m "+ " -c \""+ name+"\" " + username

def appendUserGroup( username, groupname, group):
    #print "usermod -a -G " + groupname + " " + username
    #print group[ 3]
    #if group != 0:
    #    if username in group[3]:
    #        return ''            
    return "usermod -a -G " + groupname + " " + username

def StripTags(text):
     finished = 0
     while not finished:
         finished = 1
         start = text.find("<")
         if start >= 0:
             stop = text[start:].find(">")
             if stop >= 0:
                 text = text[:start] + text[start+stop+1:]
                 finished = 0
     return text

def scan_html( filename, groupname, col_am, col_lastname, col_firstname, users, groups, run, group):
    with open(filename, "r") as input_file:
        tr = 0
        for line in input_file:
            if tr != 0:
                if line.find( "<td") != -1:
                    #Είμαστε σε στήλη
                    counter = counter + 1
                    line = StripTags( line).strip()
                    line = line.replace('&nbsp;', ' ')
                    if counter == col_am :
                        data_am = line
                    if counter == col_lastname :
                        data_lastname = line
                    if counter == col_firstname :
                        data_firstname = line
                if line.find( "</tr>") != -1:
                    tr = 0
                    name = data_lastname + " " + data_firstname
                    if (data_am < "0") or (data_am > '99999999'):
                        continue;
                    username = "u" + data_am
                    cmd = createUser(name, username, str( data_am), users)
                    dorun( cmd, run)
                    cmd = appendUserGroup( username, groupname, group)
                    dorun( cmd, run)
                    dorun( cmd, run)                      
            if tr == 0:
                if line.find( "<tr") != -1:
                    tr = 1
                    counter = -1
                    data_am = 0
                    data_lastname = ''
                    data_firstname = ''
                td = 0


def create_group( groupname, groups):
	found = 0
	for group in groups:
		if group[0] == groupname:
			found = 1
	if found == 0:
		return "groupadd " + groupname
	return ""

#Διαβάζω τους χρήστες του Ubuntu
users = []
for p in pwd.getpwall():
    users.append( p[0])

#Διαβάζω τα groups του Ubuntu
try:
    groups = grp.getgrall()
except:
    raise GroupDatabaseException(_("Failed to get the group list"))

groupname = ""
if len(sys.argv) <= 1:
    print "Παράδειγμα python import-myschool.py a.html taxi1 2 3 4"
    #Έλεγχος αν θα τρέξει κιόλας
    print "Για να εκτελεστεί θέλει sudo python ..... run"
run = 0
for param in sys.argv:
    if param == "run" :
        run = 1
    #Διαβάζω τις παραμέτρους
if len(sys.argv) >= 3:
    groupname = sys.argv[ 2]
    cmd = create_group( groupname, groups)
    dorun( cmd, run)
    col_am = int( sys.argv[ 3])
    col_lastname = int( sys.argv[ 4])
    col_firstname = int( sys.argv[ 5])    

    #Βρίσκω το group
    found = 0
    for group in groups:
        if group[0] == groupname:
            found = 1
            break 
    if found == 0:
        group = 0

    #Διαβάζω το html αρχείο
    scan_html( sys.argv[ 1], groupname, col_am, col_lastname, col_firstname, users, groups, run, group)
    scan_html( sys.argv[ 1], "students", col_am, col_lastname, col_firstname, users, groups, run, group)
            
    cmd = appendUserGroup( "administrator", groupname, group)
    dorun( cmd, run)
