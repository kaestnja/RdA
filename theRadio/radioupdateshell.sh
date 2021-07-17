#!/bin/bash
version=114
#export HOME=/home/pi
#export HOME=/root
sudo pkill -f python
sudo pkill -f python*

the_hostname=$(hostname)
echo "jk-hostname: $the_hostname"
echo "----------------------------------------------------------------"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd && echo x)" && DIR="${DIR%x}" && DIR="${DIR//$'\n'}"
echo "jk-current DIRECTORY of script: $DIR"
dir=$(pwd)
echo "jk-current directory of shell : $dir"
echo "----------------------------------------------------------------"

#add the thenewusername to the same groups as pi
#for GROUP in $(groups pi | sed 's/.*:\spi//'); do sudo adduser thenewusername $GROUP; done
#add thenewusername to sudo group:
#usermod -a -G sudo thenewusername

#sudo -H -u someUser someExe [arg1 ...]
# Example:
#sudo -H -u root env  # print the root user's environment
echo "----------------------------------------------------------------"
echo "jk-Current whoami   : `whoami`"
echo 'jk-current $USER    :' $USER
#id=$(/usr/bin/id -run)
#echo "current id: $id"
echo "jk-current id       : $(/usr/bin/id -run)"
echo "jk-Current user ids : `id`"
echo "jk-getent group user: `sudo getent group $USER`"
echo "----------------------------------------------------------------"
if [[ "${USER}" == "$(/usr/bin/id -run)" && "${USER}" == `whoami` ]] ; then
    currentuser=$USER
    echo "jk-current user: $currentuser"
    if [[ "$currentuser" == "root" || "$currentuser" == "pi"  || "$currentuser" == "root" ]] ; then
        echo "----------------------------------------------------------------"
        if [[ "$the_hostname" = "s12sky" || "$the_hostname" = "s12kali"  || "$the_hostname" = "s32kali" ]] ; then
            echo "jk-force recursive ownership for user root on his assumend home dir:/root/*"
            sudo chown -R root:root /root/*
        fi
        if [[ "$the_hostname" = "rpi1" || "$the_hostname" = "rpi2"  || "$the_hostname" = "rpi3" ]] ; then
            echo "jk-force recursive ownership for user pi on his assumend home dir:/home/pi/*"
            sudo chown -R pi:pi /home/pi/*
        fi
    else
        echo "jk-current user should be root or pi! exit now with 1"
        exit 1 
    fi
else
    echo "jk-current user could not identified completely! exit now with 1"
    exit 1    
fi
echo "----------------------------------------------------------------"
different_user=pi
#useradd -m -s /bin/bash $different_user
different_user_home=$(eval echo "~$different_user")
if [[ -d "${different_user_home}" && ! -L "${different_user_home}" ]] ; then
    if [[ -d "${different_user_home}/Desktop" && ! -L "${different_user_home}/Desktop" ]] ; then
        echo "jk-homedir Desktop of $different_user found"
    fi
    if [[ -d "${different_user_home}/Schreibtisch" && ! -L "${different_user_home}/Schreibtisch" ]] ; then
        echo "jk-homedir Schreibtisch of $different_user found"
    fi
fi
different_user=root
#useradd -m -s /bin/bash $different_user
different_user_home=$(eval echo "~$different_user")
if [[ -d "${different_user_home}" && ! -L "${different_user_home}" ]] ; then
    if [[ -d "${different_user_home}/Desktop" && ! -L "${different_user_home}/Desktop" ]] ; then
        workbench="${different_user_home}/Desktop"
        echo "jk-homedir Desktop of $different_user found: $workbench"
    fi
    if [[ -d "${different_user_home}/Schreibtisch" && ! -L "${different_user_home}/Schreibtisch" ]] ; then
        workbench="${different_user_home}/Schreibtisch"
        echo "jk-homedir Schreibtisch of $different_user found: $workbench"
    fi
    if [[ -d "${different_user_home}/Scchnurz" && ! -L "${different_user_home}/Scchnurz" ]] ; then
        workbench="${different_user_home}/Scchnurz"
        echo "jk-homedir Scchnurz of $different_user found: $workbench"
    fi
fi
echo "----------------------------------------------------------------"
#get the user name, group name, 
#and home directory of each user whose user ID is greater than or equal to 500
#sudo getent group $USER

#echo "find all accounts and their home directory:"
#while IFS=':' read -r login pass uid gid uname homedir comment; do
#    echo chown $uid:$gid "$homedir";
#done < /etc/passwd
echo "jk-find all real users and their home directory and force their ownership for:"
while IFS=':' read -r login pass uid gid uname homedir comment; do
    if [[ "$homedir" = **/home/** ]]; then
        if [[ -d "$homedir" && ! -L "$homedir" ]] ; then
            echo sudo chown -R $uid:$gid "$homedir";
            sudo chown -R $uid:$gid "$homedir";
        fi
    fi
done < /etc/passwd
echo "----------------------------------------------------------------"
#ls -l ${DIR//$'\n'}
#ls -lart ${DIR//$'\n'}

# use -H means follows symbolic links too
# change anything owned by root to pi:
#   find . -user root -exec chown pi {} \;
#change anything to user pi and group pi:
#sudo chown -R pi:pi /home/*
echo sudo chown -R ${USER:=$(/usr/bin/id -run)}:$USER ${DIR//$'\n'}
sudo chown -R ${USER:=$(/usr/bin/id -run)}:$USER ${DIR//$'\n'}
#change anything, if it is owned by user root to user pi and group pi:
#sudo chown --from=root -R pi:pi /home/*
#sudo chown --from=root -R ${USER:=$(/usr/bin/id -run)}:$USER ${DIR//$'\n'}
#change anything, if it is owned by group root to group pi:
#chown --from=:root :pi -R /home/*

#sudo chown --reference=file tmpfile

echo sudo chgrp $USER ${DIR//$'\n'}
sudo chgrp $USER ${DIR//$'\n'}

#sudo chmod -R 6777 /home/*
#sudo chmod g+x ${DIR//$'\n'}
echo sudo chmod -R 6777 ${DIR//$'\n'}
sudo chmod -R 6777 ${DIR//$'\n'}
#setfacl -m "g:root:r-x" ${DIR//$'\n'}
echo "----------------------------------------------------------------"
tempPATH="/root/Dropbox/aRadio"
if [[ -d "${tempPATH}" && ! -L "${tempPATH}" ]] ; then
    aRadioPATH=$tempPATH
fi
tempPATH="/home/pi/aRadio"
if [[ -d "${tempPATH}" && ! -L "${tempPATH}" ]] ; then
    aRadioPATH=$tempPATH
fi
tempPATH="/root/aRadio"
if [[ -d "${tempPATH}" && ! -L "${tempPATH}" ]] ; then
    aRadioPATH=$tempPATH
fi
theRadioPATH="${aRadioPATH}/theRadio"
if [[ -d "${theRadioPATH}" && ! -L "${theRadioPATH}" ]] ; then
    cd "${theRadioPATH}"
    for folder in *; do
        if [ -d "${folder}" ]; then
            echo sudo chown --from=root pi "${folder}"
            sudo chown --from=root pi "${folder}"
            echo sudo chmod -R 6777 "${folder}"
            sudo chmod -R 6777 "${folder}"
        fi
    done
    ##################################################
    cd "${theRadioPATH}"
    for file in $(printf '%s\n' *); do echo "$file"; done
    for file in *; do
        if [ -f "${file}" ]; then
            echo sudo chown --from=root pi "${file}"
            sudo chown --from=root pi "${file}"
        fi
    done
    for file in *.sh *.py; do
        if [ -f "${file}" ]; then
            echo sudo chmod -R 6777 "${file}"
            sudo chmod -R 6777 "${file}"
        fi
    done
    for file in *.desktop; do
        if [ -f "${file}" ]; then
            echo sudo cp "${file}" "${workbench}"
            if [[ -d "${workbench}" && ! -L "${workbench}" ]] ; then
                echo sudo cp "${file}" "${workbench}"
                #sudo cp "${file}" /home/pi/Desktop
            fi
        fi
    done
fi
##################################################
aFontsPATH="${theRadioPATH}/fonts"
if [[ -d "${aFontsPATH}" && ! -L "${aFontsPATH}" ]] ; then
    cd "${aFontsPATH}"
    for file in *.ttf *.otf; do
        if [ -f "${file}" ]; then
            newfile="/usr/local/share/fonts/${file}"
            if [ ! -f "${newfile}" ]; then
                echo "${file}"
                sudo chown --from=root pi "${file}"
                sudo chmod -R 6777 "${file}"
                sudo cp "${file}" /usr/local/share/fonts
            fi
        fi
    done
    sudo fc-cache
fi


##################################################
testseq="Dropbox"
if [[ $DIR == *${testseq}* ]];
then
    exit 1
fi
if [[ $dir == *${testseq}* ]];
then
    exit 1
fi
##################################################
#cat ~/.wgetrc
# cat << 'END_OF_FILE' > /home/pi/.wgetrc
# user=1172-692
# password=-Brenda+Norre0808
# END_OF_FILE
# cat /home/pi/.wgetrc

# cat << 'END_OF_FILE' > /home/pi/.wgetrc
# ftp_user=1172-692
# ftp_password=-Brenda+Norre0808
# http_user=1172-692
# http_password=-Brenda+Norre0808
# END_OF_FILE

cat ~/.netrc
touch ~/.netrc
chmod 600 ~/.netrc
echo 'machine snakekiller.de login 1172-692 password -Brenda+Norre0808' >> ~/.netrc
#touch /home/pi/.netrc
#chmod 600 /home/pi/.netrc
#echo 'machine snakekiller.de login 1172-692 password -Brenda+Norre0808' >> /home/pi/.netrc
##################################################
#https://www.krazyworks.com/wget-examples-and-scripts/
tempURL="http://snakekiller.de/download/theRadio"
if_modified_since=`date --date="2 hours ago 5 minutes ago" +%a,\ %e\ %b\ %Y\ %H:%M:%S\ GMT`
echo $if_modified_since     # Shell performs word-splitting, echo sees 6 args
#echo "$if_modified_since"   # Shell does not perform word-splitting, echo sees 1 arg

if [[ -d "${aRadioPATH}" && ! -L "${aRadioPATH}" ]] ; then
    echo "jk-start download from: $tempURL to: ${aRadioPATH}"
    cd "${aRadioPATH}"
    #wget -S -d --header="If-Modified-Since: $if_modified_since" -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -S -d -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -r -np -nH –cut-dirs=3 -R index.html http://hostname/aaa/bbb/ccc/ddd/
    #wget -r -np -nH –cut-dirs=1 -R index.html "${tempURL}"
    wget -r -np -nH –cut-dirs=1 -l2 --reject=index.html*,*.htm* -P$aRadioPATH "${tempURL}"
    #wget -S -d -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget --tries=2 --timestamping -r -nH -nc --cut-dirs=1 -l2 --no-parent '--reject=index.html*,*.htm*' -P$aRadioPATH "${tempURL}"
    #wget -E -r -l2 -nH -nc -np --cut-dirs=1 '--accept=*.desktop' '--reject=index.html*,*.htm*' "${tempURL}"
    #wget -E -r  -nH -nc -np --cut-dirs=1 -l2 --no-parent '--accept=*.desktop' '--reject=index.html*,*.htm*' -P$aRadioPATH "${tempURL}"
    #wget -r -l2 -nH -nc --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -r -l2 -nH -nc -np --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -E -k -K -nH -r -l2 --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -E -K -nH -r -l2 --cut-dirs=1 --reject="index.html*" "${tempURL}"
    #wget -m -p --adjust-extension -k -K -np "${tempURL}"
fi
exit 0
##################################################
#wget
#0 No problems occurred.
#1 Generic error code.
#2 Parse  error — for  instance,  when  parsing  command-line  options,  the  .wgetrc  or .netrc
#3 File I/O error.
#4 Network failure.
#5 SSL verification failure.
#6 Username/password authentication failure.
#7 Protocol errors.
#8 Server issued an error response.
##################################################
#tempPATH="/home/pi/aRadio"
#tempURL="http://snakekiller.de/download/theRadio"
#if_modified_since=`date --date="2 hours ago 5 minutes ago" +%a,\ %e\ %b\ %Y\ %H:%M:%S\ GMT`
#echo $if_modified_since     # Shell performs word-splitting, echo sees 6 args
###echo "$if_modified_since"   # Shell does not perform word-splitting, echo sees 1 arg
#cd "${tempPATH}" && wget -S -d --header="If-Modified-Since: $if_modified_since" -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
#cd "${tempPATH}" && wget -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"

#VERSION=${VERSION:-"$(wget --header=Accept-Encoding:identity -O - http://www.adobe.com/software/flash/about/ 2>/dev/null | fgrep -m 1 -A 2 "Firefox - NPAPI" | tail -1 | sed s/\</\>/g | cut -d\> -f3 -d ' ')"}
#VERSION=${VERSION:-"$(wget -O - http://www.adobe.com/software/flash/about/ 2>/dev/null | sed -n "/Firefox - NPAPI/{N;p}" | tr -d ' '| tail -1 | tr '<>' '  ' | cut -f3 -d ' ')"}
#echo "Latest version = "$VERSION



#cd "${tempPATH}" && sudo wget --user=1172-692 --password=-Brenda+Norre0808 -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
#cd "${tempPATH}" && sudo wget --user=1172-692 --password=-Brenda+Norre0808 --auth-no-challenge -r -l2 -nH --cut-dirs=1 --reject="index.html*" "${tempURL}"
##################################################
#Say you would like to download a file so that it keeps its date of modification.
#wget -S http://www.gnu.ai.mit.edu/ 
#Several days later, you would like Wget to check if the remote file has changed, and download it if it has.
#wget -N http://www.gnu.ai.mit.edu/
##################################################
#wget -m www.ilanni.com/nexus/content/
#wget --mirror -pc --convert-links -P ./your-local-dir/ http://www.your-website.com
##################################################
# get the login page to get the hidden field data
#wget -a log.txt -O loginpage.html http://foobar/default.aspx
#hiddendata=`grep value < loginpage.html | grep foobarhidden | tr '=' ' ' | awk '{print $9}' | sed s/\"//g`
#rm loginpage.html
# login into the page and save the cookies
#postData=user=fakeuser'&'pw=password'&'foobarhidden=${hiddendata}
#wget -a log.txt -O /dev/null --post-data ${postData} --keep-session-cookies --save-cookies cookies.txt http://foobar/default.aspx
# get the page your after
#wget -a log.txt -O results.html --load-cookies cookies.txt http://foobar/lister.aspx?id=42
#rm cookies.txt
##################################################
# tempPATH="/home/pi/aRadio/theRadio"
# tempURLfile="http://snakekiller.de/download/theRadio/radiopy.py"
# tempPATHfilenew="/home/pi/aRadio/theRadio/radiopy.py"
# tempPATHfileold="/home/pi/aRadio/theRadio/radiopy.py"
# cd "${tempPATH}" && sudo wget --timestamping "${tempURLfile}"
# if [ $(stat -c '%Y' $tempPATHfilenow) -gt $(stat -c '%Y' $tempPATHfileold) ]; then
    # gzip -cd file.csv.gz > file.csv
# fi
##################################################
#tempFILE="radioupdateshell.sh"
#tempPATH="/home/pi/aRadio/theRadio/"
#tempURL="http://snakekiller.de/download/"
#cd "${tempPATH}" && wget "${tempURL}${tempFILE}"
#if [ -f "${tempPATH}${tempFILE}" ]; then
#    echo "got file: ${tempPATH}${tempFILE}"
#fi
##################################################
theRadioPATH=$aRadioPATH + '/theRadio'
if [[ -d "${theRadioPATH}" && ! -L "${theRadioPATH}" ]] ; then
    cd "${theRadioPATH}"
    for folder in *; do
        if [ -d "${folder}" ]; then
            echo sudo chown --from=root pi "${folder}"
            sudo chown --from=root pi "${folder}"
            echo sudo chmod -R 6777 "${folder}"
            sudo chmod -R 6777 "${folder}"
        fi
    done
    ##################################################
    cd "${theRadioPATH}"
    for file in $(printf '%s\n' *); do echo "$file"; done
    for file in *; do
        if [ -f "${file}" ]; then
            echo sudo chown --from=root pi "${file}"
            sudo chown --from=root pi "${file}"
        fi
    done
    for file in *.sh *.py; do
        if [ -f "${file}" ]; then
            echo sudo chmod -R 6777 "${file}"
            sudo chmod -R 6777 "${file}"
        fi
    done
    for file in *.desktop; do
        if [ -f "${file}" ]; then
            echo sudo cp "${file}" /home/pi/Desktop
            sudo cp "${file}" /home/pi/Desktop
        fi
    done
fi
##################################################
aFontsPATH=$theRadioPATH + 'fonts'
if [[ -d "${aFontsPATH}" && ! -L "${aFontsPATH}" ]] ; then
    cd "${aFontsPATH}"
    for file in *.ttf *.otf; do
        if [ -f "${file}" ]; then
            newfile="/usr/local/share/fonts/${file}"
            if [ ! -f "${newfile}" ]; then
                echo "${file}"
                sudo chown --from=root pi "${file}"
                sudo chmod -R 6777 "${file}"
                sudo cp "${file}" /usr/local/share/fonts
            fi
        fi
    done
    sudo fc-cache
fi
##################################################
#python3 /home/pi/aRadio/theRadio/radiopy.py &
python3 $theRadioPATH/radiopy.py &
##################################################
exit 0
##################################################
#create menu entry via .desktop file
echo "[Desktop Entry]
Name=CubicSDR
GenericName=CubicSDR
Comment=Software Defined Radio
Exec=/opt/CubicSDR/CubicSDR
Icon=/opt/CubicSDR/CubicSDR.ico
Terminal=false
Type=Application
Categories=Network;HamRadio;" > /usr/share/applications/cubicsdr.desktop
##################################################
##################################################
tempFILELIST="/home/pi/aRadio/theRadio/radiodesktopfiles.txt"
#printf '%s\n' *
#printf '%s\n' *.desktop
#cd "${tempPATH}" && printf '%s\n' *.desktop >"radiodesktopfiles.txt"
#cd "${tempPATH}" && printf '%s\n' *.desktop >${tempFILELIST}
#xargs --arg-file=radiodesktopfiles.txt cp --target-directory=/home/pi/Desktop
#xargs --arg-file=${tempFILELIST} cp --target-directory=/home/pi/Desktop
#files=($(< radiodesktopfiles.txt))
#files=($(< ${tempFILELIST}))
#for file in $(<radiodesktopfiles.txt); do cp "$file" /home/pi/Desktop; done
#for file in $(<${tempFILELIST}); do echo cp "$file" /home/pi/Desktop; done
#for file in $(printf '%s\n' *.desktop); do echo cp "$file" /home/pi/Desktop; done
while read -r line; do for file in $line; do cp "$file" new_folder; done; done < radiodesktopfiles.txt
for file in "${files[@]}"; do 
    #wget "${uri}${file}"
    cp "$file" /home/pi/Desktop
done

FILE="/home/pi/theRadio/test_tkinter.py"

if [ -f "$FILE" ]; then
    echo "File $FILE found."
    python3 "$FILE" &
    exit 0
else
    echo "File $FILE not found."
    FILE="/root/Dropbox/aRadio/theRadio/test_tkinter.py"
    if [ -f "$FILE" ]; then
        echo "File $FILE found."
        python3 "$FILE" &
        exit 0
    else
        echo "File $FILE not found."
    fi
fi
exit 1

tempPATH="/home/pi/aRadio"
tempURL="http://snakekiller.de/download/theRadio"
#cd "${tempPATH}" && wget -O - "${tempURL}"
#cd "${tempPATH}" && wget --max-redirect=20 -O "${tempPATH}" "${tempURL}"
#cd "${tempPATH}" && wget --max-redirect=20 -O "${tempURL}" "${tempPATH}"
#cd "${tempPATH}" && wget -r --no-parent "${tempURL}"
#cd "${tempPATH}" && wget -r --no-parent -e robots=off "${tempURL}" "${tempPATH}"
#cd "${tempPATH}" && wget -r -l2 --no-parent "${tempURL}" "${tempPATH}"
#cd "${tempPATH}" && wget -r -l2 -nH "${tempURL}"

#if [ ! -f "$FILE" ]; then
#-b filename - Block special file
#-c filename - Special character file
#-d directoryname - Check for directory Existence
#-e filename - Check for file existence, regardless of type (node, directory, socket, etc.)
#-f filename - Check for regular file existence not a directory
#-G filename - Check if file exists and is owned by effective group ID
#-G filename set-group-id - True if file exists and is set-group-id
#-k filename - Sticky bit
#-L filename - Symbolic link
#-O filename - True if file exists and is owned by the effective user id
#-r filename - Check if file is a readable
#-S filename - Check if file is socket
#-s filename - Check if file is nonzero size
#-u filename - Check if file set-user-id bit is set
#-w filename - Check if file is writable
#-x filename - Check if file is executable
