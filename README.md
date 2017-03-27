# PiOven

Python library and program to make a Raspberry Pi control a glass annealing oven.

a.	Sensor: MAX13855 thermocouple amplifier w/ type K thermocouple
https://www.adafruit.com/product/269 

b.	Relay to control elements: FOTEK SSR-40DA.
http://www.fotek.com.hk/solid/SSR-1.htm 

Breadboard diagram is included in images directory. (SSR shown in diagram is not the FOTEK SSR-40DA.)

TODO:  
[] Setup \\ Install documents  
[] Accept oven configuration filename and program filename as arguements when calling PiOvenProgram.py  
[] Impliment interrupts: NEXTSTEP and STOPNOW  
[] Impliment HOLD as time for instructions in \*\_prog.json  
[] Impliment saftey checks based on oven configuration  
[] Make wrappers to operate from the web interface, create in subdir of cgi-bin  
