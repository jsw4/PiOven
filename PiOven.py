# -*- coding: utf-8 -*-#
import json
import time
import RPi.GPIO as GPIO
import Adafruit_MAX31855.MAX31855 as MAX31855
import rrdtool
import PiOvenConfig as cfg


# Raspberry Pi software SPI configuration.
# These are the pins I have the thermocouple connected to
CLK = 25
CS  = 24
DO  = 18
thermocouple = MAX31855.MAX31855(CLK, CS, DO)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

class sensor(object):
	"""Data from a thermocouple and the chip/computer at a given point of time

	attributes:
		oven: the temperature of the thrmocouple (F)
                room: the temperatur at Max13855 (F)
	"""

	def __init__(self):
		"""return a new sensor object"""

	        self.oven = 1.8 * thermocouple.readTempC() +32
	        self.room = 1.8 * thermocouple.readInternalC() +32

        def refresh(self):
                self.oven = 1.8 * thermocouple.readTempC() +32
	        self.room = 1.8 * thermocouple.readInternalC() +32
	        return self

class elements(object):
	"""The elements in the oven are controlled by a relay.

	attributes:
		status: on or off
	
	methods:
		on: turn the relay on
		off: turn the relay on
		refresh: update the status attribute
		cleanup: cleanup the GPIO status
	"""

	def __init__(self):
		"""Return a new elements object"""		
		self.status = GPIO.input(16)

	def refresh(self):
		"""update the status attribute of elements object"""
		self.status = GPIO.input(16)
		return self

	def on(self):
                """turn on the element"""
	        GPIO.output(16, True)
	        self.status = GPIO.input(16)
	        log(cfg.log_filename, 'Elements turned on')
	        print "heat on" #testing output
	        return self

	def off(self):
                """turn off the element"""
	        GPIO.output(16, False)
	        self.status = GPIO.input(16)
	        log(cfg.log_filename, 'Elements turned off')
	        print "heat off" #testing output 
	        return self


        #def __del__(self):
	def cleanup(self):
                GPIO.cleanup()
                return 'GPIO is cleaned up. (OFF)'

class wrstatus(object):
	"""write the status of the program. 

	attributes:
		status_file_name: a json file named current_status.json
		time: time of the status
		oven_temp: temp in the oven
		room_temp: temp outside the oven
		calc_temp: calculated target temp for this time
		element_status: status of elements (on/off)
		program_name: name of the oven program
		program_step_number: which step of the oven program is being executed
		graph_url: path to the png file calculated from the graphfile + cfg.graph_url
		
	methods:
		delete_file:
	"""

        def __init__(self, status_file_name, program_name, program_step_number, calc_temp, graphfile):
                self.time = time.ctime()
                s = sensor()
                self.oven_temp = s.oven
                self.room_temp = s.room
                self.calc_temp = calc_temp
                e = elements()
                self.element_status = e.status 
                self.program_name = program_name
                self.program_step_number = program_step_number
                self.graph_url = str(cfg.graph_url) + str(graphfile)

                try:
                        sf = open(status_file_name, "w")
                        sf.write(json.dumps(self,
                                            default=lambda o: o.__dict__,
                                            sort_keys=True,
                                            indent=4))
                        sf.close
                except IOError:
                        return False

                # self.rrdslug = rrdslug

                # rrdtool.update(str(self.rrdslug), 'N:%s:%s:%s' %(self.oven_temp,self.room_temp,self.calc_temp))

class log(object):
        """write an entry to the log
        todo - this is really a function, not an object
        
        """
        def __init__(self, logfile, event):
                line = time.ctime() + " " + str(event) +"\n"
                try: 
                        lf = open(logfile, "a+")
                        lf.write(line)
                        lf.close()

                except IOError:
                        return False
        
class file2obj(object):
        """read a json file and return object representing json
        
        """
        def __init__(self, json_file_name):
                # TODO : Validate json_file_name -> exists -> is JSON
                try:
                        with open(json_file_name) as json_data:
                                dictionary = json.load(json_data)
                                for k, v in dictionary.iteritems():
                                    setattr(self, k, v)
                except IOError:
                        return False


class line(object):
        """ takes a single program step and calculates slope function

        """
        def __init__(self, endpoint, last_temp):
                for k, v in endpoint.iteritems():
                        setattr(self, k, v)
                self.y1 = float(last_temp)
                self.x1 = 0 # now
                self.y2 = float(self.temp)
                self.x2 = float(self.time)
                try:
                        self.slope = (self.y2 - self.y1) / (self.x2 - self.x1)
                except ZeroDivisionError:
                        self.slope = 'INF'
                        
                if (self.y1 < self.y2):
                        self.slopedir = 'UP'
                elif (self.y1 > self.y2):
                        self.slopedir = 'DOWN'
                else:
                        self.slopedir = 'HORIZ'

