#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os

dirname = "/etc/cron.weekly";
try:
    os.stat(dirname)
except:
    os.mkdir(dirname)
filename = dirname + "/fstrim"
with open(filename, "w") as text_file:    
    text_file.write("#! /bin/sh\n");
    text_file.write("\n");
    text_file.write("# By default we assume only / is on an SSD.\n");
    text_file.write("# You can add more SSD mount points, separated by spaces.\n");
    text_file.write("# Make sure all mount points are within the quotes. For example:\n");
    text_file.write("\n");
    text_file.write("SSD_MOUNT_POINTS='/'  \n");
    text_file.write("\n");
    text_file.write("for mount_point in $SSD_MOUNT_POINTS\n");
    text_file.write("do\n");
    text_file.write("\tfstrim -v $mount_point  \n");
    text_file.write("done\n");
cmd = "chmod +x /etc/cron.weekly/fstrim";
os.system( cmd);
cmd = "/etc/cron.weekly/fstrim";
os.system( cmd);

    
