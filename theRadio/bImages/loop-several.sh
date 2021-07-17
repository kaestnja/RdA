#!/bin/bash
echo -e "\e[?17;0;0c"
clear
while true;
do
for file in $1*
do
omxplayer  -o local "$file" > /dev/null
done
done
