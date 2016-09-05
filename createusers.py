#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2012 Fotis Tsamis <ftsamis@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import pwd, grp, os, crypt

def createUser(name, username, password):
    encPass = crypt.crypt(password,"22")   
    return os.system("useradd -p "+encPass+ " -s "+ "/bin/bash "+ "-d "+ "/home/" + username+ " -m "+ " -c \""+ name+"\" " + username)

def create_usernames( computers, tmimata1, count):
	usernames = []
	for computer in computers:
		for tmima in tmimata1:
			username = 'erg' + computer + tmima
			usernames.append( username)
	return usernames


#Δημιουργεί ένα group με το όνομα groupname
def create_group( groupname, groups):
	found = 0
	for group in groups:
		if group[0] == groupname:
			found = 1
	if found == 0:
		print "Create group "  + groupname
		os.system("groupadd " + groupname)
	return found

def append_user_to_group( username, groupname, group):
    if username not in group[3]:
        print "append " + username + " to group " + groupname
        os.system("usermod -a -G " + groupname + " " + username)
					
#Φτιάχνω τους χρήστες
def create_users(groupname, tmimata, usernames):
	#Αρχικά φτιάχνω το group με όνομα groupname
    try:
        groups = grp.getgrall()
    except:
        raise GroupDatabaseException(_("Failed to get the group list"))	        
    create_group( groupname, groups)

    #Πρέπει να φτιάξω ένα group ανά τμήμα
    for tmima in tmimata:
        if tmima != '':
            create_group( tmima, groups)
            
    #Πρέπει να ξαναδιαβάσω τα groups γιατί έφτιαξα και νέα
    try:
        groups = grp.getgrall()
    except:
        raise GroupDatabaseException(_("Failed to get the group list"))    

	#Στη συνέχεια φτιάχνω τους χρήστες
    users = []
    for p in pwd.getpwall():
        users.append( p[0])
    for username in usernames:
        if( username not in users):
            print "createuser " + username
            createUser( username, username, username)

	#Βάζω τους χρήστες στο κατάλληλο group
    usernames.append( "administrator")
    for group in groups:
        if group[0] == groupname:
            for username in usernames:
                append_user_to_group( username, groupname, group)

    #Πρέπει να τους βάλω στο group του τμήματος
    for group in groups:
        for tmima in tmimata:
            if group[0] == tmima:
                #Βρήκα το group του τμήματος
                for username in usernames:
                    if username[ -2:] == tmima:
                        append_user_to_group( username, tmima, group)


tmimata = ['', 'a1', 'a2', 'b1']
computers = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']

#computers = ['a1', 'b1']
usernames = create_usernames( computers, tmimata, 4)
print usernames
#Η πρώτη παράμετρος είναι το όνομα του group στο οποίο θα ανήκουν όλοι οι μαθητές (το τμήμα της τάξης δηλαδή)
create_users( "erg", tmimata, usernames)


