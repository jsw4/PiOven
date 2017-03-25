# -*- coding: utf-8 -*-#

### Paths
# datapath = DIR where data and configuration files are stored
#data_path = '/var/www/html/data/'
data_path = '/var/PiOven/'
# path to where graphs are output
graph_path = '/var/www/html/graphs/'
# WEB path to where graphs are output (same directory as above)
graph_url = '/graphs/'

### Files
status_filename = data_path + '/current_status.json'
log_filename = data_path + '/PiOven.log'
oven_conf_filename = data_path + '/boxoven_conf.json'
program_filename = data_path + '/ezbake_prog.json'

### RRD Strings - funtions that return lists of strings
def createstr(maxtemp): 
	maxtemp = str(maxtemp)
	return [ 
		'--step', '60',
               	'DS:oventemp:GAUGE:600:0:' + maxtemp,
               	'DS:chiptemp:GAUGE:600:0:' + maxtemp,
               	'DS:calctemp:GAUGE:600:0:' + maxtemp,
               	'RRA:AVERAGE:0:1:86400'
		]

def graphstr(slug, title):
        title = str(title)
	return [
	      '--imgformat', 'PNG',
              '--step', '60',
              '--start', 'end-8h',
              '--width', '480',
              '--height', '180',
              '--vertical-label', 'Temp (deg F)',
              '--title', title,
              '--lower-limit', '55',
              str('DEF:OvenTemp=' + slug + ':oventemp:AVERAGE'),
              str('DEF:ChipTemp=' + slug + ':chiptemp:AVERAGE'),
              str('DEF:CalcTemp=' + slug + ':calctemp:AVERAGE'),
              'AREA:OvenTemp#119911:Oven Temperature',
              'AREA:ChipTemp#111199:MAX13855 Temperature',
              'LINE2:CalcTemp#991111:Target Temperature'
		]
