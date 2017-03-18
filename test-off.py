import PiOven

x = PiOven.sensor()

print str(x.oven) + " " + str(x.room)

y = PiOven.elements()

y.off()
y.refresh() # get status refreshed

print "status " + str(y.status)

