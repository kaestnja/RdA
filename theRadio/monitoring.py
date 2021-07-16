#!/usr/bin/python
from __future__ import division
from subprocess import PIPE, Popen
import psutil


def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def main():
    cpu_temperature = get_cpu_temperature()
    print('CpuTemp = {0:0.2f} C'.format(cpu_temperature))
    cpu_usage = psutil.cpu_percent(0.1, False)
    print('CpuUsage = {0:0.2f} %'.format(cpu_usage))
    print('CpuCount = {0:0.0f}'.format(psutil.cpu_count()))
    #freqs = psutil.cpu_freq()
    #print('CpuFreqCurrent = {0:0.2f} %'.format(freqs.current))
    #print('CpuFreqMin = {0:0.2f} %'.format(freqs.min))
    #print('CpuFreqMax = {0:0.2f} %'.format(freqs.max))

    ram = psutil.virtual_memory()
    ram_total = ram.total / 2**20       # MiB.
    print('RamTotal = {0:0.2f} MB'.format(ram_total))
    ram_used = ram.used / 2**20
    print('RamUsed = {0:0.2f} MB'.format(ram_used))
    ram_free = ram.free / 2**20
    print('RamFree = {0:0.2f} MB'.format(ram_free))
    ram_available = ram.available / 2**20
    print('RamAvailable = {0:0.2f} MB'.format(ram_available))
    ram_percent_used = ram.percent
    print('RamPercent = {0:0.2f} %'.format(ram_percent_used))

    disk = psutil.disk_usage('/')
    disk_total = disk.total / 2**30     # GiB.
    print('DiskTotal = {0:0.2f} GB'.format(disk_total))
    disk_used = disk.used / 2**30
    print('DiskUsed = {0:0.2f} GB'.format(disk_used))
    disk_free = disk.free / 2**30
    print('DiskFree = {0:0.2f} GB'.format(disk_free))
    disk_percent_used = disk.percent
    print('DiskPercent = {0:0.2f} %'.format(disk_percent_used))



if __name__ == '__main__':
    main()