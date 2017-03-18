import PiOven

x = PiOven.sensor()

print str(x.oven) + " " + str(x.room)

y = PiOven.elements()

y.on()

y.refresh()

print "status " + str(y.status)
