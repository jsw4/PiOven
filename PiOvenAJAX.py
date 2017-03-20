#!/usr/bin/python
# -*- coding: utf-8 -*-#

# library path (needs PiOven.py)
lib_path = '/home/pi/PiOven'
# data path
data_path = '/var/www/html/data/'
# full path to oven configuration file
ocf_name = data_path + 'boxoven_conf.json'
# full path to annealing program
apf_name = data_path + 'ezbake_prog.json'
# full path to status file
# csf_name = data_path + 'current_status.json'
csf_name = data_path + 'current_status.json'
# end of user conf

import sys
sys.path.append(lib_path)
import PiOven
import json

status = PiOven.file2obj(csf_name)

print "Content-Type:application/json\n\n"
print json.dumps({
  "time": status.time,
  "oven_temp": status.oven_temp,
  "chip_temp": status.room_temp,
  "element_status": status.element_status,
  "program_name": status.program_name,
  "program_step_number": status.program_step_number,
  "graph_url": status.graph_url
  },
indent=4,
sort_keys=True,
separators=(',', ': ')
                 )
