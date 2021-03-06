#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import pwd, grp, os, crypt, os, getpass, stat, shutil

def createUser(name, username, password):
    encPass = crypt.crypt(password,"22")   
    return os.system("useradd -p "+encPass+ " -s "+ "/bin/bash "+ "-d "+ "/home/" + username+ " -m "+ " -c \""+ name+"\" " + username)

def create_usernames( computers, tmimata1):
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
def create_users(groupname, computers, tmimata):
    usernames = create_usernames( computers, tmimata)
    #print usernames

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
                append_user_to_group( "administrator", tmima, group)
                for username in usernames:
                    if username[ -2:] == tmima:
                        append_user_to_group( username, tmima, group)
                    if username[ -3:] == tmima:
                        append_user_to_group( username, tmima, group)                        
                        
def create_change_tmima( tmimata):
    tmimata.append( "xo")
    username = getpass.getuser()
    dirname = os.environ['HOME'] + "/Επιφάνεια εργασίας/Αλλαγή τμήματος";
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)    
    for tmima in tmimata:
        filename = dirname + "/" + tmima + ".sh"
        with open(filename, "w") as text_file:    
            text_file.write( "#!/bin/sh\n")
            text_file.write( "# $0 is the script name\n")
            text_file.write( "\n")
            text_file.write( "me=`basename \"$0\"`\n")
            text_file.write( "sudo python lts.py ${me%.*}\n")
            text_file.write( "read -p \"Πατήστε Enter\" yn \n")
        os.chmod( filename, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    shutil.copy2( "lts.py", dirname + "/lts.py")       

def make_scripts():
    dirname = "/scripts"
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)
    #os.system( "sudo chown  administrator /scripts/;sudo chgrp  administrator /scripts/")
    
    #filename = dirname + "/init-client-mate.sh"
    #with open(filename, "w") as text_file:
    #    text_file.write( "python /scripts/createremmina.py\n")
    #    text_file.write( "dconf load /org/mate/panel/ < /scripts/panel-client-mate.txt\n")
    #os.system( "chown administrator /scripts/createremmina.py;chmod 777 /scripts/createremmina.py")
    #shutil.copy2( "scripts/createremmina.py", "/scripts/createremmina.py")
    #os.system( "chown administrator scripts/createremmina.py")



def init_users( groupname, computers, tmimata):
    #sudo ltsp-update-image -c /
    usernames = create_usernames( computers, tmimata)
    for username in usernames:
        cmd = "sudo -u " + username + " ./scripts/init-client-mate.sh"
        #os.system( cmd)
        print cmd

computers = ['a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'c1', 'c2', 'c3', 'c4', 'c5', 'd1', 'd2', 'd3', 'd4', 'd5']
tmimata = ['']
create_users( "erg", computers, tmimata)
if len(tmimata) > 1:
    create_change_tmima( tmimata)
#make_scripts()
init_users( "erg", computers, tmimata)
