#!/bin/bash
 
rm -rf /opt/adobe-air-sdk
rm -rf /opt/airapps
mkdir ~/scratch2
cd ~/scratch2
wget http://airdownload.adobe.com/air/lin/download/2.6/AdobeAIRSDK.tbz2
mkdir /opt/adobe-air-sdk
sudo tar jxf AdobeAIRSDK.tbz2 -C /opt/adobe-air-sdk
wget https://aur.archlinux.org/cgit/aur.git/snapshot/adobe-air.tar.gz
tar xvf adobe-air.tar.gz -C /opt/adobe-air-sdk
chmod +x /opt/adobe-air-sdk/adobe-air/adobe-air
mkdir /opt/adobe-air-sdk/scratch
wget https://scratch.mit.edu/scratchr2/static/sa/Scratch-456.0.4.air
cp Scratch-456.0.4.air /opt/adobe-air-sdk/scratch/
mkdir /tmp/Scratch
cp Scratch-456.0.4.air /tmp/Scratch
cd /tmp/Scratch
unzip /tmp/Scratch/Scratch-456.0.4.air
cp /tmp/Scratch/icons/AppIcon128.png /opt/adobe-air-sdk/scratch/scratch.png
cd ~/scratch2
rm -rf /tmp/Scratch
cat << _EOF_ > /usr/share/applications/Scratch2.desktop
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Exec=/opt/adobe-air-sdk/adobe-air/adobe-air /opt/adobe-air-sdk/scratch/Scratch-456.0.4.air
Icon=/opt/adobe-air-sdk/scratch/scratch.png
Terminal=false
Name=Scratch 2
Comment=Programming system and content development tool
Categories=Application;Education;Development;ComputerScience;
MimeType=application/x-scratch-project
_EOF_
chmod +x /usr/share/applications/Scratch2.desktop
echo "Done"
