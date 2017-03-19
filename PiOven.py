# -*- coding: utf-8 -*-#
import json
import time
import RPi.GPIO as GPIO
import Adafruit_MAX31855.MAX31855 as MAX31855

class sensor(object):
	"""Data from a thermocouple and the chip/computer at a given point of time

	attributes:
		oven: the temperature of the thrmocouple (F)
                room: the temperatur at Max13855 (F)
	"""

	def __init__(self):
		"""return a new sensor object"""

	        # Raspberry Pi software SPI configuration.
	        # These are the pins I have the thermocouple connected to
	        CLK = 25
        	CS  = 24
        	DO  = 18
        	max = MAX31855.MAX31855(CLK, CS, DO)

	        self.oven = 1.8 * max.readTempC() +32
	        self.room = 1.8 * max.readInternalC() +32


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
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(16, GPIO.OUT)
		self.status = GPIO.input(16)

	def refresh(self):
		"""update the status attribute of elements object"""
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(16, GPIO.OUT)
		self.status = GPIO.input(16)
		return self

	def on(self):
                """turn on the element"""
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(16, GPIO.OUT)
	        GPIO.output(16, True)
	        #should be logged
	        print "heat on" #testing output
	        return self

	def off(self):
                """turn off the element"""
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(16, GPIO.OUT)
	        GPIO.output(16, False)
	        # should be logged
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
		element_status: status of elements (on/off)
		program_name: name of the oven program
		program_step_number: which step of the oven program is being executed
		graph_url: path to the png file calculated from slug.
	
	methods:
		delete_file:
	"""

        def __init__(self, status_file_name, program_name, program_step_number, html_url):
                self.time = time.ctime()
                s = sensor()
                self.oven_temp = s.oven
                self.room_temp = s.room
                e = elements()
                self.element_status = e.status 
                self.program_name = program_name
                self.program_step_number = program_step_number
                self.graph_url = html_url

                try:
                        sf = open(status_file_name, "w")
                        sf.write(json.dumps(self,
                                            default=lambda o: o.__dict__,
                                            sort_keys=True,
                                            indent=4))
                        sf.close
                except IOError:
                        return False

class log(object):
        """write an entry to the log
        
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




