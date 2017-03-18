# -*- coding: utf-8 -*-#
# this file is not used anymore
class graph(object):
	"""wrapper style RRD data and graphing interface for PiOven
        which makes it a wrapper around a wrapper... no real savings.

	attributes:
		createstr: list of strings for RRD creation
		graphstr: list of strings for RRD graphing
		datastr: list of data to insert into RRD

	methods:
		make: makes the PNG
		datapoint: puts data in RRD
	"""
	def __init__(self, createstr):            
                import rrdtool

                self.createstr = createstr

                rrdtool.create(self.createstr)

                self.graphstr = None
                self.datastr = None
                
        def make(self, graphstr):
                import rrdtool
                rrdtool.graph(graphstr)
                return

        def datapoint(self, datastr):
                import rrdtool
                rrdtool.update(datastr)
                return
                
class interrupt(object):
	"""Gets input from file and acts on it during execution of the program.
	this is how the PiOvenProgram gets input while running
	file is named 'interrupt.json' (something else creates this file)

	attributes:
		action: what to do. accept limited number of things, ignore the rest.
	"""

	def __init__(self):
		intfile = 'interrupt.json'
		import json
		import os
		try:
			with open(intfile) as oven_intr:
				x = json.load(oven_intr)
				self.action = x["action"]
			os.remove(intfile)
		except IOError:
			self.action = "none"

class sit(object):
	"""DEPRICATED write to file status for web app to read
	also write to a logfile 

	attributes:
		success:record worked or it didn't

	"""
	def _init_(self, event):
		self.success = True

	def rep(self, event):
		# logfile = "/var/log/PiOven.log" pi can't do it
		logfile = '/home/pi/PiOven/PiOven.log'
		import time
		line = time.ctime() + " " + str(event) +"\n"
		try: 
			lf = open(logfile, "a+")
			lf.write(line)
			lf.close()
			self.success = True
		except IOError:
			self.success = False
		return self
