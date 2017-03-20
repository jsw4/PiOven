# -*- coding: utf-8 -*-#

# libpath = DIR where the python library(s) are
lib_path = '/home/pi/PiOven'

# todo : accept 'boxoven' and 'ezbake' (or whatever) as inputs

import sys
try:
    sys.path.index(lib_path)
except ValueError:
    sys.path.append(lib_path)
import PiOven
import PiOvenConfig as cfg
import rrdtool
import time
import os  

if not PiOven.log(cfg.log_filename, 'PiOven Program initializing'):
    sys.exit('Problem with the PiOven log file')

if os.path.isfile(cfg.status_filename):
    PiOven.log(cfg.log_filename, 'A PiOven program is already running, only one can run at a time')
    sys.exit('PiOven program already running.')

oven = PiOven.file2obj(cfg.oven_conf_filename)
program = PiOven.file2obj(cfg.program_filename)
sensor = PiOven.sensor()
elements = PiOven.elements()

# setup the RRD stuff
slug = oven.slug + '-' + program.slug + '-' + time.strftime("%m%H%M")
rrdslug = cfg.data_path + slug + '.rrd'
graphslug = cfg.graph_path + slug + '.png'
graphstr = cfg.graphstr(rrdslug)

rrdtool.create(str(rrdslug), cfg.createstr)

last_temp = sensor.oven

for endpoint in program.endpoints:
    line = PiOven.line(endpoint,last_temp)
    # we get line.x1 ... line.y2 and line.slope, line.step, line.temp, line.time
    # program.endpoints.index(endpoint) = array index
    
    if line.slope == 'INF':
        # on until the temp is reached
        print 'INF to ' + str(line.temp) # remove after testing
        while line.temp > sensor.oven:
            elements.on()
            PiOven.wrstatus(cfg.status_filename, program.name, line.step, '/graphs/' + slug + '.png', str(line.temp), rrdslug)
            time.sleep(60)
            # dont forget to graph each time... this has to be possible in a big mega func
            
        # off until the temp is reached
        else:
            elements.off()
            PiOven.wrstatus(cfg.status_filename, program.name, line.step, '/graphs/' + slug + '.png', str(line.temp), rrdslug)
            time.sleep(60)

    # slope is not INF
    else:
        start_t = time.time()
        end_t = startime + (int(line.time) * 60)
        while end_t > time.time():
            target_temp = line.slope * ((time.time() - start_t) * 60) + last_temp
            print tartget_temp # remove after testing
            if sensor.oven() < target_temp:
                elements.on()
                PiOven.wrstatus(
                                cfg.status_filename,
                                program.name,
                                line.step,
                                '/graphs/' + slug + '.png',
                                str(target_temp),
                                rrdslug
                                )
                time.sleep(60)
            else:
                elements.on()
                PiOven.wrstatus(
                                cfg.status_filename,
                                program.name,
                                line.step,
                                '/graphs/' + slug + '.png',
                                str(target_temp),
                                rrdslug
                                )
                time.sleep(60)

    last_temp = line.temp # for the next line
    
PiOven.log(cfg.log_filename, str(elements.cleanup()))

os.remove(cfg.status_filename)
PiOven.log(cfg.log_filename, 'Status file is removed; PiOven program has cleanly exited')
