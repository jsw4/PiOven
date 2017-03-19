# -*- coding: utf-8 -*-#

### Paths
# libpath = DIR where the python library(s) are
lib_path = '/home/pi/PiOven'
# datapath = DIR where data and configuration files are stored
data_path = '/var/www/html/data'
# path to where graphs are output
graph_path = '/var/www/html/graphs/'

### Files
status_filename = data_path + '/current_status.json'
log_filename = data_path + '/PiOven.log'
oven_conf_filename = data_path + '/boxoven_conf.json'
program_filename = data_path + '/ezbake_prog.json'
# todo : accept 'boxoven' and 'ezbake' as inputs

import rrdtool
import time
import os  
import sys
try:
    sys.path.index(lib_path)
except ValueError:
    sys.path.append(lib_path)
import PiOven

if not PiOven.log(log_filename, 'PiOven Program initialized'):
    sys.exit('Problem with the PiOven log file')

if os.path.isfile(status_filename):
    PiOven.log(log_filename, 'A PiOven program is already running, only one can run at a time')
    sys.exit('PiOven program already running.')

oven = PiOven.file2obj(oven_conf_filename)
PiOven.log(log_filename, oven.name +': oven configuration loaded')

program = PiOven.file2obj(program_filename)
PiOven.log(log_filename, program.name +': oven program loaded')
# todo : return the acutal steps

# todo : make unique slug for rrd files

PiOven.wrstatus(status_filename, program.name, 0, '/graphs/example-graph.png')

# todo: run each step of the program

i = 10
while i > 0:
    print i
    time.sleep(2)
    i = i - 1

e = PiOven.elements()

PiOven.log(log_filename, str(e.cleanup()))

os.remove(status_filename)
PiOven.log(log_filename, 'Status file is removed; PiOven program has cleanly exited')
