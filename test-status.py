import PiOven

x = PiOven.sensor()

print str(x.oven) + " " + str(x.room)

y = PiOven.elements()

print "status " + str(y.status)
