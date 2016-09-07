#!/bin/sh
# $0 is the script name

me=`basename "$0"`
echo ${me%.*}
sudo python lts.py ${me%.*}
read -p "Πατήστε Enter" yn
