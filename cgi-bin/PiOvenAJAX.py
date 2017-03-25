#!/usr/bin/python
# -*- coding: utf-8 -*-#

lib_path = '/home/pi/PiOven/'

import sys
sys.path.append(lib_path)
import PiOven
import PiOvenConfig as cfg
import json

status = PiOven.file2obj(cfg.status_filename)

print "Content-Type:application/json\n\n"
print json.dumps({
  "time": status.time,
  "oven_temp": status.oven_temp,
  "chip_temp": status.room_temp,
  "calc_temp": status.calc_temp,
  "element_status": status.element_status,
  "program_name": status.program_name,
  "program_step_number": status.program_step_number,
  "graph_url": status.graph_url
  },
indent=4,
sort_keys=True,
separators=(',', ': ')
                 )
