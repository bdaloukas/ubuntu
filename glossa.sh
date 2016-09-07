cd $(mktemp -d)
wget -q 'http://alkisg.mysch.gr/steki/index.php?action=dlattach;topic=4061.0;attach=2539' -O glossa.zip
unzip -O cp737 glossa.zip
sudo cp *.exe /usr/share/glossa/glossa.exe

