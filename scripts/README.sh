
## Working dir
LINK=/Users/lavieestuntoucan/Civilia/projets/Saguenay/tech/openTripPlanner/input
cd $LINK

## Input directory must contain:
## (1) OpenStreetMap file (Saguenay.osm.pbf)
## (2) zipped gtfs file (gtfs.zip)

## Create the routes with a gtfs
java -Xmx1G -jar otp-1.2.0-shaded.jar --build $LINK/otp

## Analyse with these routes
java -Xmx1G -jar otp-1.2.0-shaded.jar --server --basePath $LINK --router otp --analyst  --port 55555 --securePort 55556 

## Run OTP with script
## Needed (hard-coded):
## (1) link to graph directory
## (2) origin-destination-time files
## (3) name of output file
jython -Dpython.path=otp-1.2.0-shaded.jar batch_OTP.py

