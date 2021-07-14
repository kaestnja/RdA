#!/bin/bash
cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000))
cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))

echo CPU temp"="$cpuTemp1"."$cpuTempM"'C"
echo GPU $(/opt/vc/bin/vcgencmd measure_temp)

#############################################
gpuTemp0=$(/opt/vc/bin/vcgencmd measure_temp)
gpuTemp0=${gpuTemp0//\'/?}
gpuTemp0=${gpuTemp0//temp=/}

echo CPU Temp: $cpuTemp1"."$cpuTempM"?C"
echo GPU Temp: $gpuTemp0

#sudo apt-get install bc
#echo "scale=1; $(cat /sys/class/thermal/thermal_zone0/temp)/1000" | bc


