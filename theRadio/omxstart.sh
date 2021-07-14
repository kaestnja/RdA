#!/bin/bash
#echo -n '-' > /var/omx_fifo
sleep 5  #This ensures that the LXDE session has started up fully before attempting to open the file
exec xterm -fn fixed -fullscreen -fg black -bg black -e omxplayer -o hdmi --no-osd --loop -r "$1""
