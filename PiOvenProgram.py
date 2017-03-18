# -*- coding: utf-8 -*-#

# libpath = DIR where the python library(s) are
libpath = '/home/pi/PiOven'
# datapath = DIR where data and configuration files are stored
datapath = '/var/www/html/data'
status_file_name = datapath + '/current_status.json'
log_file_name = datapath + '/PiOven.log'
# htmlpath DIR where graph / HTML output is stored
html_path = '/var/www/html/graphs'
# URL of DIR where graphs and HTML is stored
html_url_base = '/graphs/'

import rrdtool
import time
import os  
import sys
try:
    sys.path.index(libpath)
except ValueError:
    sys.path.append(libpath)
import PiOven

if not PiOven.log(log_file_name, 'PiOven Program initialized'):
    sys.exit('Problem with the PiOven log file')

if os.path.isfile(status_file_name):
    PiOven.log(log_file_name, 'A PiOven program is already running, only one can run at a time')
    sys.exit('PiOven program already running.')

# get/open oven configuration

# get/open the program

# run each step of the program

# PiOven.status(status_file_name, 'not loaded yet', 0, '/graphs/snail2.png')

# end of program
e = PiOven.elements()

PiOven.log(log_file_name, str(e.cleanup()))

os.remove(status_file_name)
PiOven.log(log_file_name, 'Status file is removed; PiOven program has cleanly exited')







