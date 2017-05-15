#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import pwd, grp, os, crypt, os, getpass, stat, shutil

def createUser(name, username, password):
    encPass = crypt.crypt(password,"22")   
    cmd = "useradd -p "+encPass+ " -s "+ "/bin/bash "+ "-d "+ "/home/" + username+ " -m "+ " -c \""+ name+"\" " + username
    print cmd
    return os.system( cmd)


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
def create_users(groupname, frompc, topc):
    #usernames = create_usernames( computers, tmimata)
    #print usernames

	#Αρχικά φτιάχνω το group με όνομα groupname
    try:
        groups = grp.getgrall()
    except:
        raise GroupDatabaseException(_("Failed to get the group list"))	        
    create_group( groupname, groups)

    #Πρέπει να φτιάξω ένα group ανά τμήμα
    #for tmima in tmimata:
    #    if tmima != '':
    #        create_group( tmima, groups)
            
    #Πρέπει να ξαναδιαβάσω τα groups γιατί έφτιαξα και νέα
    try:
        groups = grp.getgrall()
    except:
        raise GroupDatabaseException(_("Failed to get the group list"))    

    #Στη συνέχεια φτιάχνω τους χρήστες
    users = []
    usernames = ['administrator']
    for p in pwd.getpwall():
        users.append( p[0])
    for i in range(frompc, topc+1):
        password = str( i / 10) + str( i % 10)
        username = "pc" + password
        usernames.append( username)
        if( username not in users):
            createUser( username, username, password)                

    #Βάζω τους χρήστες στο κατάλληλο group
    for group in groups:
        if group[0] == groupname:
            for username in usernames:
                append_user_to_group( username, groupname, group)


create_users( "erg", 1, 15)
