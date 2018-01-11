#!/usr/bin/jython

from org.opentripplanner.scripting.api import *
import csv

# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/Users/lavieestuntoucan/Civilia/projets/Saguenay/tech/openTripPlanner/graphs", "--router", "otp-scenario4" ])
resultFile = 'simResult_otp-scenario4.csv'

# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter()
# Create a default request for a given departure time
req = otp.createRequest()
req.setMaxTimeSec(7200)                   # set a limit to maximum travel time (seconds)
#req.setModes('WALK,BUS,RAIL')             # define transport mode
#req.setSearchRadiusM(500)                 # set max snapping distance to connect trip origin to street network
req.maxWalkDistance = 1000                 # set maximum walking distance ( kilometers ?)
# req.walkSpeed = walkSpeed                 # set average walking speed ( meters ?)
# req.bikeSpeed = bikeSpeed                 # set average cycling speed (miles per hour ?)

# Read Points of Destination - The file points.csv contains the columns GEOID, X and Y.
ori = otp.loadCSVPopulation('input/ori-od.csv', 'Y', 'X')
dest = otp.loadCSVPopulation('input/des-od.csv', 'Y', 'X')
hredep = list(csv.reader(open('input/hredep-od.csv'), delimiter=','))

# Create a CSV output
matrixCsv = otp.createCSVOutput()
matrixCsv.setHeader([ 'trip', 'walk_distance', 'travel_time', 'boardings' ])

# Start Loop
i=0
for o,d in zip(ori,dest):

    print("---")
    print(i)
    i = i + 1

    hre=int(hredep[i][0])
    min=int(hredep[i][1])
    if hre >= 24: hre = hre - 24

    if hre <= 6: continue 
    req.setDateTime(2017, 12, 4, hre, min, 00)

    req.setOrigin(o)
    spt = router.plan(req) 
    if spt is None: continue 
    r = spt.eval(d) 
    if r is None: continue
    w  = r.getWalkDistance()
    if w is None: w = -1
    matrixCsv.addRow([ r.getIndividual().getStringData('GEOID'), round(w) , r.getTime(),  r.getBoardings() ])
 # Save the result
matrixCsv.save(resultFile)

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
