#32-bit:
cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86" | tar xzf -

#64-bit:
cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -

#Führen Sie den Dropbox-Daemon danach von dem neuen .dropbox-dist -Ordner aus aus.
~/.dropbox-dist/dropboxd




sudo apt-key adv --keyserver pgp.mit.edu --recv-keys 5044912E
sudo add-apt-repository "deb http://linux.dropbox.com/ubuntu $(lsb_release -sc) main"
sudo apt-get update
sudo apt-get install dropbox