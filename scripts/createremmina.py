#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (C) 2016 Vasilis Daloukas <bdaloukas@gmail.com>
# License GNU GPL version 3 or newer <http://gnu.org/licenses/gpl.html>

import os,getpass,socket
import base64    
from Crypto.Cipher import DES3

REMMINAPREF_SECRET_B64=b'TJTk6d+qJghaWCE8Xl4M+CED6ZZ+XUkjRD/B+0jyDJU='

def create_file_pref():
    username = getpass.getuser()
    dirname = os.environ['HOME'] + "/.remmina";
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)
    filename = dirname + "/remmina.pref"
    with open(filename, "w") as text_file:
        text_file.write("[remmina_pref]\n")
        text_file.write("secret=" + REMMINAPREF_SECRET_B64 + "\n")
        text_file.write("save_view_mode=true\n")
        text_file.write("save_when_connect=true\n")
        text_file.write("invisible_toolbar=false\n")
        text_file.write("always_show_tab=true\n")
        text_file.write("hide_connection_toolbar=false\n")
        text_file.write("default_action=0\n")
        text_file.write("scale_quality=3\n")
        text_file.write("hide_toolbar=false\n")
        text_file.write("hide_statusbar=false\n")
        text_file.write("show_quick_search=false\n")
        text_file.write("small_toolbutton=false\n")
        text_file.write("view_file_mode=0\n")
        text_file.write("resolutions=640x480,800x600,1024x768,1152x864,1280x960,1400x1050\n")
        text_file.write("main_width=600\n")
        text_file.write("main_height=400\n")
        text_file.write("main_maximize=false\n")
        text_file.write("main_sort_column_id=3\n")
        text_file.write("main_sort_order=0\n")
        text_file.write("expanded_group=\n")
        text_file.write("toolbar_pin_down=false\n")
        text_file.write("sshtunnel_port=4732\n")
        text_file.write("applet_new_ontop=false\n")
        text_file.write("applet_hide_count=false\n")
        text_file.write("applet_enable_avahi=false\n")
        text_file.write("minimize_to_tray=false\n")
        text_file.write("recent_maximum=10\n")
        text_file.write("default_mode=0\n")
        text_file.write("tab_mode=0\n")
        text_file.write("auto_scroll_step=10\n")
        text_file.write("hostkey=65508\n")
        text_file.write("shortcutkey_fullscreen=102\n")
        text_file.write("shortcutkey_autofit=49\n")
        text_file.write("shortcutkey_nexttab=65363\n")
        text_file.write("shortcutkey_prevtab=65361\n")
        text_file.write("shortcutkey_scale=115\n")
        text_file.write("shortcutkey_grab=65508\n")
        text_file.write("shortcutkey_minimize=65478\n")
        text_file.write("shortcutkey_disconnect=65473\n")
        text_file.write("shortcutkey_toolbar=116\n")
        text_file.write("vte_font=\n")
        text_file.write("vte_allow_bold_text=true\n")
        text_file.write("vte_lines=512\n")

def encryptRemminaPass(plain):
    plain = plain.encode('utf-8')
    secret = base64.b64decode(REMMINAPREF_SECRET_B64)
    key = secret[:24]
    iv = secret[24:]
    plain = plain + b"\0" * (8 - len(plain) % 8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    result = cipher.encrypt(plain)
    result = base64.b64encode(result)
    result = result.decode('utf-8')
    return result
    
def get_password( username):
    if len(username) > 5:
        username = username[:5] 
    password = encryptRemminaPass( username)
    return password
    
def create_file_remmina( ip):
    username = getpass.getuser()
    filename = os.environ['HOME'] + "/.remmina/1473068943832.remmina"
    with open(filename, "w") as text_file:
        text_file.write("[remmina]\n")
        text_file.write("disableclipboard=0\n")
        text_file.write("ssh_auth=0\n")
        text_file.write("clientname=\n")
        text_file.write("quality=9\n")
        text_file.write("ssh_charset=\n")
        text_file.write("ssh_privatekey=\n")
        text_file.write("sharesmartcard=0\n")
        text_file.write("resolution=\n")
        text_file.write("group=\n")
        text_file.write("password=" + get_password( username) + "\n")
        text_file.write("name=winxp\n")
        text_file.write("ssh_loopback=0\n")
        text_file.write("shareprinter=0\n")
        text_file.write("ssh_username=\n")
        text_file.write("ssh_server=\n")
        text_file.write("security=rdp\n")
        text_file.write("protocol=RDP\n")
        text_file.write("execpath=\n")
        text_file.write("sound=local\n")
        text_file.write("exec=\n")
        text_file.write("username=" + username + "\n")
        text_file.write("sharefolder=\n")
        text_file.write("console=0\n")
        text_file.write("domain=\n")
        text_file.write("server=" + ip + "\n")
        text_file.write("colordepth=16\n")
        text_file.write("viewmode=4\n")
        text_file.write("window_maximize=1\n")

create_file_pref()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect( ("8.8.8.8", 0))
ip = s.getsockname()[0]
pos = ip.rfind( ".")
ip = ip[ 0: pos+1]+"20"
create_file_remmina( ip)

