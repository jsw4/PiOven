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
slug = oven.slug + '-' + program.slug + '-' + time.strftime("%m%d%H%M")
rrdslug = cfg.data_path + slug + '.rrd'
graphslug = cfg.graph_path + slug + '.png'
graphstr = cfg.graphstr(rrdslug)
createstr = cfg.createstr(oven.maxsafetemp)

rrdtool.create(str(rrdslug), createstr)

last_temp = sensor.oven

for endpoint in program.endpoints:
    line = PiOven.line(endpoint,last_temp)
    # we get line.x1 ... line.y2 and line.slope, line.step, line.temp, line.time
    # program.endpoints.index(endpoint) = array index
    # logging ... 

    start_t = time.time()
    if line.slope == 'INF':
        # max preheat time in minutes
        end_t = start_t + (int(oven.maxpreheattime) * 60)
    else:        
        end_t = start_t + (int(line.time) * 60)

    q = 0
    while end_t > time.time():
        
        if q == 5:
            end_t = time.time()
            continue # end of infinte up/down program step 
        
        if line.slope == 'INF':
            target_temp = line.temp
        else:
            target_temp = line.slope * ((time.time() - start_t) / 60) + last_temp       

        punc = ':'
        rrdtool.update(str(rrdslug),
                       punc.join(
                           ('N', str(sensor.oven), str(sensor.room), str(target_temp)
                            )))
        rrdtool.graph(str(graphslug), graphstr)

        q = 0
        while (q < 4):
            
            f = 0
            while (f < 3):
                time.sleep(5)
                # every 5 seconds
                sensor.refresh()
                # todo : saftey check
                # todo : interupt check
                f = f + 1
            
            # every 15 seconds (3 x 5 second loop)
            print 'target ' + str(target_temp), line.slopedir, 'current ' + str(sensor.oven) # remove when done testing
            if sensor.oven >= target_temp:
                # todo : only turn on if we are off
                # todo : add a log entry in the object (update the class method) when this happens.
                elements.off()
                if line.slope == 'INF' and line.slopedir == 'UP' :
                    print 'done inf up line' # remove when done testing
                    q = 4
            else:
                # todo : only turn off if we are on
                # log this too
                elements.on()
                if line.slope == 'INF' and line.slopedir == 'DOWN' :
                    print 'done inf up line' # remove later (did you really test down?)
                    q = 4
                
            PiOven.wrstatus(cfg.status_filename, program.name, line.step, target_temp, rrdslug)
            q = q + 1
        # every minute (4 x 15 second loop)
        
        print 'end of the minute cycle', start_t - time.time()
        
    # time is over or temperature is reached.

    # if time is over but temperature is not reached
    # sys.exit('Preheat / cooldown time exceeded program ending.)

    # log the end of an oven program instruction / line.
        
    last_temp = line.temp # for the next line
    
PiOven.log(cfg.log_filename, str(elements.cleanup()))

os.remove(cfg.status_filename)
# remove the rrd too
PiOven.log(cfg.log_filename, 'Status file is removed; PiOven program has cleanly exited')
