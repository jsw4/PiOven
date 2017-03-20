# -*- coding: utf-8 -*-#

### Paths
# datapath = DIR where data and configuration files are stored
data_path = '/var/www/html/data/'
# path to where graphs are output
graph_path = '/var/www/html/graphs/'

### Files
status_filename = data_path + '/current_status.json'
log_filename = data_path + '/PiOven.log'
oven_conf_filename = data_path + '/boxoven_conf.json'
program_filename = data_path + '/ezbake_prog.json'

### RRD Strings (be carefull)
createstr = [ '--step', '60',
               'DS:oventemp:GAUGE:180:0:100',
               'DS:chiptemp:GAUGE:180:0:100',
               'DS:calctemp:GAUGE:180:0:100',
               'RRA:AVERAGE:0:1m:6h']


#graphstr = [ mypipath + slug + '.png',
# cheats (be really carefull)
def graphstr(slug):
	return [
	      '--imgformat', 'PNG',
              '--start', 'end-3h',
              '--step', '60',
              '--width', '360',
              '--height', '100',
              '--vertical-label', 'Temp',
              '--title', 'Test Pi Oven Cycle Graph',
              '--lower-limit', '0',
              'DEF:OvenTemp=' + slug + ':oventemp:AVERAGE',
              'DEF:ChipTemp=' + slug + ':chiptemp:AVERAGE',
              'AREA:OvenTemp#009900:Oven Temperature',
              'AREA:ChipTemp#000099:Chip Temperature',
              'LINE:ChipTemp#990000:Chip Temperature',
		   ]
