#!/bin/bash
echo "17" > /sys/class/gpio/export
echo "in" >/sys/class/gpio/gpio17/direction
chmod 666 /sys/class/gpio/gpio17/direction
chmod 666 /sys/class/gpio/gpio17/value

LED="0"; OLD="0"; CNT="0"
while :
do
  LED=$(cat /sys/class/gpio/gpio17/value)
  echo -n $LED
  if [ $LED -ne "0" ]; then CNT=$(($CNT + 1)); fi
  if [ $OLD -eq "1" -a $LED -eq "0" ]; then
    if [ $CNT -gt 13 ]; then
      echo " *1*"
    elif [ $CNT -gt 4 ]; then
      echo " *0*"
    else
      echo " *x*"
    fi
    CNT="0"
  fi
  OLD=$LED
done
