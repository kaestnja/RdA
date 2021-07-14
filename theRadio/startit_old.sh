DISPLAY=:0.0; export DISPLAY
#export DISPLAY=<your.own.ip>:0.0
#export DISPLAY=:0.0
#echo $XDG_RUNTIME_DIR
export XDG_RUNTIME_DIR=/run/user/1000
#log directory: /home/pi/.cache/lxsession/LXDE-pi
#log path: /home/pi/.cache/lxsession/LXDE-pi/run.log
#tail -n30 /home/pi/.cache/lxsession/LXDE-pi/run.log

#sudo apt-get install -y gobject-introspection
#sudo apt-get install -y libgirepository1.0-dev
#sudo apt-get install -y libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
#sudo apt-get install -y libssl-dev
#sudo python3 -m pip install -U --force-reinstall cryptography
#sudo python3 -m pip install objgraph
#sudo python3 -m pip install resource
#C:\Users\Jan\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\rootfs\root

/mnt/c/Program Files/Microsoft VS Code/bin/code
/usr/bin/code

sudo apt-get install -y libcurl4-openssl-dev
sudo apt-get install -y python-igraph
sudo apt-get install -y libxml2
sudo python3 -m pip install --ignore-installed pycairo pygobject
sudo python3 -m pip install --ignore-installed systemd-python
sudo pip3 install --upgrade --ignore-installed --proxy 141.73.108.181:8080 pyyaml
sudo apt install -y libgirepository1.0-dev
sudo http_proxy='http://141.73.108.181:8080/' apt install -y libgirepository1.0-dev
sudo http_proxy='http://user:pass@141.73.108.181:8080/' apt install -y libgirepository1.0-dev

            #sudo apt install -y libgirepository1.0-dev
            #sudo apt-get install -y libcurl4-openssl-dev
            #sudo apt-get install -y python-igraph
            #sudo apt-get install -y libxml2
            #sudo python3 -m pip install --ignore-installed pycairo pygobject
            #sudo python3 -m pip install --ignore-installed systemd-python
            
            sudo python3 -m pip freeze > requirements.txt
            sudo python3 -m pip uninstall -r requirements.txt
            sudo python3 -m pip uninstall -r requirements.txt -y
            for r in $(cat requirements.txt | grep -v ^#); do pip uninstall -y $r; done;
            for r in $(cat requirements.txt | grep -v ^#); do python3 -m pip uninstall -y $r; done;
            #sudo python3 -m pip freeze | xargs pip uninstall -y
            #sudo python3 -m pip freeze | grep -v "^-e" | xargs pip uninstall -y
            python3 -m pip uninstall -y -r <(sudo python3 -m pip freeze)
            
            

the_hostname=$(hostname)
sudo python3 -m pip list > ~/pip3_installed_$the_hostname.log
sudo python -m pip list > ~/pip_installed_$the_hostname.log

sudo python3 -m pip list --no-cache-dir --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo python3 -m pip install -U > ~/pip3_updated_$the_hostname.log
sudo python -m pip list --no-cache-dir --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo python -m pip install -U > ~/pip_updated_$the_hostname.log
exit 0   

/home/pi/aRadio/theRadio/startit_switch.sh &
#/home/pi/aRadio/theRadio/startit_switch.sh > /dev/null 2>&1

# ./my_program

# ./my_program 2>&1

# ./my_program 2>&1 | cat

# strace -ewrite -o trace.txt -s 2048 ./my_program; sed 's,^[^"]*"\(.*\)"[^"]*$,\1,g;s,\\n,,g;' trace.txt > mytrace.txt
# cat mytrace.txt

KILLCOUNTER=0
while true
do
    cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
    cpuTemp1=$(($cpuTemp0/1000))
    cpuTemp2=$(($cpuTemp0/100))
    cpuTempM=$(($cpuTemp2 % $cpuTemp1))
    #echo CPU temp: $cpuTemp1
    #gpuTemp=$(/opt/vc/bin/vcgencmd measure_temp)
    #echo GPU $gpuTemp
    #############################################
    #awk -v a="$(awk '/cpu /{print $2+$4,$2+$4+$5}' /proc/stat; sleep 1)" '/cpu /{split(a,b," "); print 100*($2+$4-b[1])/($2+$4+$5-b[2])}'  /proc/stat
    cpu_util2a="$(awk -v a="$(awk '/cpu /{print $2+$4,$2+$4+$5}' /proc/stat; sleep 1)" '/cpu /{split(a,b," "); print 100*($2+$4-b[1])/($2+$4+$5-b[2])}'  /proc/stat)"
    cpu_util2=${cpu_util2a%.*}
    #printf " Current CPU Utilization2 : %s\n" "$cpu_util2"
    #############################################
    # Read /proc/stat file (for first datapoint)
    read cpu user nice system idle iowait irq softirq steal guest< /proc/stat
    # compute active and total utilizations
    cpu_active_prev=$((user+system+nice+softirq+steal))
    cpu_total_prev=$((user+system+nice+softirq+steal+idle+iowait))
    #sleep 0.05
    sleep 1
    # Read /proc/stat file (for second datapoint)
    read cpu user nice system idle iowait irq softirq steal guest< /proc/stat
    # compute active and total utilizations
    cpu_active_cur=$((user+system+nice+softirq+steal))
    cpu_total_cur=$((user+system+nice+softirq+steal+idle+iowait))
    # compute CPU utilization (%)
    cpu_util1=$((100*( cpu_active_cur-cpu_active_prev ) / (cpu_total_cur-cpu_total_prev) ))
    #printf " Current CPU Utilization1 : %s\n" "$cpu_util1" 
    #############################################
    if [ $cpuTemp1 -lt 57 ] && ([ $cpu_util1 -lt 50 ] || [ $cpu_util2 -lt 50 ]); then
    #if [ $cpuTemp1 -lt 60 ] && [ $cpu_util2 -lt 50 ]; then
        KILLCOUNTER=0
        if pgrep -x "python3" > /dev/null
        then
            #echo "python3 still running"
            sleep 10
        else
            SWITCHc=$(cat /sys/class/gpio/gpio18/value)
            if [ $SWITCHc -eq "0" ]; then
                #rm /home/pi/.cache/lxsession/LXDE-pi/run.log
                #date >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                #echo "--- start Python script1 and wait 120s ---" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                #echo "--- CPU temp  : $cpuTemp1" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                #echo GPU $gpuTemp
                #echo "--- CPU util 1: $cpu_util1" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                #echo "--- CPU util 2: $cpu_util2" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                #python3 /home/pi/aRadio/theRadio/anneradio.py > /dev/null &
                python3 /home/pi/aRadio/theRadio/anneradio.py > /dev/null 2>&1
                sleep 120
                if pgrep -x "python3" > /dev/null
                then
                    sleep 1
                    #echo "--- python3 runns now ---" >> /home/pi/.cache/lxsession/LXDE-pi/run.log;
                fi
            fi
        fi
        # if pgrep -x "python3" > /dev/null
        # then
            # echo "Python Running"
        # else
            # echo "start Python script2"
            # DISPLAY=:0 python3 /home/pi/aRadio/theRadio/anneradio.py &
            # sleep 10
        # fi
        # if pgrep -x "python3" > /dev/null
        # then
            # echo "Python Running"
        # else
            # echo "start Python script3"
            # DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/anneradio.py
            # sleep 10
        # fi
    else
        sleep 10
        #date >> /home/pi/.cache/lxsession/LXDE-pi/run.log
        #echo "--- to hot -- or -- to much load --" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
        #echo "--- KILLCOUNTER   : $KILLCOUNTER" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
        #echo "--- CPU temp  : $cpuTemp1" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
        #echo GPU $gpuTemp
        #echo "--- CPU util 1: $cpu_util1" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
        #echo "--- CPU util 2: $cpu_util2" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
        #(( KILLCOUNTER++ ))
        #((KILLCOUNTER+=1))
        KILLCOUNTER=$((KILLCOUNTER+1))
        if [ $KILLCOUNTER -gt 7 ]; then
            #date >> /home/pi/.cache/lxsession/LXDE-pi/run.log
            echo "------ for more than 10s x 6 ---- kill python3 and omxplayer now --" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
            KILLCOUNTER=0
            if pgrep -x "python3" > /dev/null
            then
                #echo "------ killing python3 ---" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                pkill -f python3
            fi
            if pgrep -x "omxplayer" > /dev/null
            then
                #echo "------ killing omxplayer ---" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                pkill omxplayer
            fi
            sleep 20
            if pgrep -x "python3" > /dev/null
            then
                #echo "------ killing python3 again ---" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                sudo pkill -SIGKILL -f python3
            fi
            if pgrep -x "omxplayer" > /dev/null
            then
                #echo "------ killing omxplayer again ---" >> /home/pi/.cache/lxsession/LXDE-pi/run.log
                sudo pkill -SIGKILL -f omxplayer
            fi        
            # pkill -f python*
            # pkill -f python
            # sudo pkill -f python
            # sudo pkill -f omxplayer
            # sudo pkill -SIGKILL -f python3
        fi
    fi
done

exit 0

Check_ntp () {
    echo "Checking the NTP Service Status on $(uname -n)"
    ps -e | grep ntp > /dev/null 2>&1
    if [ $? -eq 0 ] ; then
    echo "Service Status:  NTP Service is Running"
    else
    echo "Service Status:  NTP Service is Not Running"
    fi
    }

#  cd /root/aRadio/theRadio && python3 radiopy.py
#/sys/class/thermal/thermal_zone0/temp
#omxplayer --blank /home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4 &
#omxplayer -o local '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4' --win '0 0 800 480'
#DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4'
#exec xterm -fn fixed -fullscreen -fg black -bg black -e omxplayer -o hdmi --no-osd --loop -r "$1""

#http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_GPIO_Shell.html
sudo usermod -a -G gpio root
sudo usermod -a -G gpio pi
sudo su
echo "18" > /sys/class/gpio/export
chmod 660 /sys/class/gpio/gpio18/direction
chmod 660 /sys/class/gpio/gpio18/value
echo "in" > /sys/class/gpio/gpio18/direction
echo 1 >/sys/class/gpio/gpio18/active_low
su pi
ls /sys/class/gpio
cat /sys/class/gpio/gpio18/value

sudo nano /etc/rc.local
usermod -a -G gpio root
usermod -a -G gpio pi
echo "18" > /sys/class/gpio/export
chmod 660 /sys/class/gpio/gpio18/direction
chmod 660 /sys/class/gpio/gpio18/value
echo "in" > /sys/class/gpio/gpio18/direction
echo 1 >/sys/class/gpio/gpio18/active_low


usermod -a -G gpio root
usermod -a -G gpio pi
echo "18" > /sys/class/gpio/export
echo "22" > /sys/class/gpio/export
chmod 660 /sys/class/gpio/gpio18/direction
chmod 660 /sys/class/gpio/gpio22/direction
chmod 660 /sys/class/gpio/gpio18/value
chmod 660 /sys/class/gpio/gpio22/value
echo "in" > /sys/class/gpio/gpio18/direction
echo "in" > /sys/class/gpio/gpio22/direction
echo 1 >/sys/class/gpio/gpio18/active_low
echo 0 >/sys/class/gpio/gpio22/active_low



    Mit dem Kommando 
ls /sys/class/gpio 
    können Sie nun ein neues Verzeichnis mit dem Namen 'gpio23' sehen. 
    In diesem Verzeichnis befinden sich u. a. zwei Dateien direction und value. 
    Diese Dateien dienen zum Steuern des GPIO-Pins. 
    Nun wird entschieden, ob der GPIO-Port Eingang oder Ausgang sein soll, z.B.: 
    Eingang:
echo "in" > /sys/class/gpio/gpio23/direction
Val=$(cat /sys/class/gpio/gpio18/value)
    oder zum invertieren:
echo 1 >/sys/class/gpio/gpio23/active_low
    Wenn active_low auf 1 gesetzt ist, liegt am Pin "0" an, wenn in value "1" steht, und umgekehrt. 
    Ausgang:
echo "out" > /sys/class/gpio/gpio23/direction
echo "0" > /sys/class/gpio/gpio23/value

#!/bin/sh
# sudo nano /etc/rc.local
# Input-Ports (Taster)
for Port in  17 27
  do
  echo "$Port" > /sys/class/gpio/export
  echo "in" >/sys/class/gpio/gpio${Port}/direction
  chmod 660 /sys/class/gpio/gpio${Port}/direction
  chmod 660 /sys/class/gpio/gpio${Port}/value
done

# Output-Ports (LED)
for Port in 22 23 24 25
  do
  echo "$Port" > /sys/class/gpio/export
  echo "out" >/sys/class/gpio/gpio${Port}/direction
  echo "0" >/sys/class/gpio/gpio${Port}/value
  chmod 660 /sys/class/gpio/gpio${Port}/direction
  chmod 660 /sys/class/gpio/gpio${Port}/value
done

if [ -n "$IF_WPA_IFACE" ]; then


# quit if executables are not installed
if [ ! -x "$WPA_SUP_BIN" ] || [ ! -x "$WPA_CLI_BIN" ]; then
    exit 0
fi

do_start () {
    if test_wpa_cli; then
        # if wpa_action is active for this IFACE, do nothing
        ifupdown_locked && exit 0

        # if the administrator is calling ifup, say something useful
        if [ "$PHASE" = "pre-up" ]; then
            wpa_msg stderr "wpa_action is managing ifup/ifdown state of $WPA_IFACE"
            wpa_msg stderr "execute \`ifdown --force $WPA_IFACE' to stop wpa_action"
        fi
        exit 1
    elif ! set | grep -q "^IF_WPA"; then
        # no wpa- option defined for IFACE, do nothing
        exit 0
    fi

    # ensure stale ifupdown_lock marker is purged
    ifupdown_unlock

    # preliminary sanity checks for roaming daemon
    if [ -n "$IF_WPA_ROAM" ]; then
        if [ "$METHOD" != "manual" ]; then
            wpa_msg stderr "wpa-roam can only be used with the \"manual\" inet METHOD"
            exit 1
        fi
        if [ -n "$IF_WPA_MAPPING_SCRIPT" ]; then
            if ! type "$IF_WPA_MAPPING_SCRIPT" >/dev/null; then
                wpa_msg stderr "wpa-mapping-script \"$IF_WPA_MAPPING_SCRIPT\" is not valid"
                exit 1
            fi
        fi
        if [ -n "$IF_WPA_MAPPING_SCRIPT_PRIORITY" ] && [ -z "$IF_WPA_MAPPING_SCRIPT" ]; then
            wpa_msg stderr "\"wpa-mapping-script-priority 1\" is invalid without a wpa-mapping-script"
            exit 1
        fi
        IF_WPA_CONF="$IF_WPA_ROAM"
        WPA_ACTION_SCRIPT="/sbin/wpa_action"
    fi
}
case "$MODE" in 
    start)
        do_start
        case "$PHASE" in
            pre-up)
                kill_wpa_supplicant
                init_wpa_supplicant    || exit 1
                conf_wpa_supplicant     || { kill_wpa_supplicant; exit 1; }
                ;;
            post-up)
                init_wpa_cli         || { kill_wpa_supplicant; exit 1; }
                ;;
        esac
        ;;

    stop)
        do_stop
        case "$PHASE" in
            pre-down)
                kill_wpa_cli
                ;;
            post-down)
                kill_wpa_supplicant
                ;;
            *)
                wpa_msg stderr "unknown phase: \"$PHASE\""
                exit 1
                ;;
        esac
        ;;

    *)
        wpa_msg stderr "unknown mode: \"$MODE\""
        exit 1
        ;;
esac

exit 0
