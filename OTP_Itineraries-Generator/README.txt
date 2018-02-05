## OTP_Itineraries-Generator

This scripts takes in input origin/destination csv files and outputs one json file per trip containing all the
data given by OTP as well as a csv files containing the following data :
    tripID,itinerary_nb, duration,start_time, end_time, walk_time, walk_distance, transit_time,
    waiting_time, boardings, bus_lines_numbers, boarding_stop_ids, debarquer_stop_ids
The json files are placed in a directory called OIG_jsonResults itself placed at the project root
The csv file is placed in a directory called OIG_csvResults itself placed at the project root

A text file containing the trip options may be included in the OIG project directory.  Here's how to format it:
    - Any line starting with the character '#' will be skipped (as well as empty lines)
    - Trip options must be written as 'option_name:value' with no space at any place in the line.
      option_name must be typed exactly as in the following list, otherwise it will have no effect.
    - The trip options are (each are explained in the given options file) :
        	maxWalkDistance, maxHours, mode, numItineraries, walkSpeed, carSpeed,
                walkReluctance, stairsReluctance, waitReluctance, waitAtBeginningFactor, ignoreRealtimeUpdates

Two optional file are contain in OTP_Itineraries-Generator, namely CmdPrinter and Timer.  The first one is a
pretty printer for the loading process and the second is a writes the Elapsed Time of the process at the end.
Both can be removed without causing any problems

The Elapsed Time of the project highly depends on the length of the OD files and your internet connection.


## HOW TO RUN OTP_Itineraries-Generator

(1) Make sure python 3 is installed on your computer

(2) Start an instance of OpenTripPlanner
	(2.1) Direct to the directory containing the otp shaded.jar file
	(2.2) Type : java -Xmx2G -jar otp-X.Y.Z-shaded.jar --build $LINK --inMemory
		(2.2.1) Where otp-X.Y.Z-shaded.jar is the otp shaded.jar name
		(2.2.2) $LINK is the directory containing the gtfs and osm files
		(2.2.3) Note that -Xmx2G represent the memory allocated to OTP, no less than 1G can be given (ie -Xmx1G)
			and this parameter can be omited (if so, OTP will have no memory limit)

(3) Open a new terminal

(4) Direct into the directory containing the file named "OIG-main.py"

(5) Type : py OIG-main.py $OD-LINK $SERVER $DOWNLOAD_JSON
	(5.1) $OD-LINK is the path to that od csv files (from root)
	(5.2) (Optional) $SERVER is the server port where otp is currently running 
		-(if none is specified in the otp launch line [step (2.2)], don't specify here either, default is 8080)
	(5.3) (Optional) If $DOWNLOAD_JSON is 'false' the JSON file won't be downloaded from OTP API and it will
	      	be assumed that the json files are already downloaded and are located in a directory named OIG_jsonResults
		in the project root
		- For testing purposes
		- If anything other than 'false' is specified, the json files will be downloaded




========================================================================================================================

**************************
*       IMPORTANT        *
**************************
The OD directory needs to contain the followings :

		1. CSV file containing the origin data in the format 	  : id, lat, lon
                   The origin file name MUST CONTAIN 'ori' (and must NOT contain 'des' or 'h')
			- Note that the first row must not contain any important data as it will be skipped

		2. CSV file containing the destination data in the format : id, lat, lon
                   The destionation file name MUST CONTAIN 'des' (and must NOT contain 'ori' or 'h')
			- Note that the first row must not contain any important data as it will be skipped

		3. (Optional) CSV file containing the departure hours for every OD point
                   If the hours file is included, it's name MUST CONTAIN 'h' (and must NOT contain 'ori' or 'des')
			- Note that the first row MAY CONTAIN data, as it will NOT be skipped
			- Can be in the format : id, hour, minute
			- Can be in the format : hour, minute 
				(in this case, the time will be match to the Origin data placed at the same line, 
				so it is advised to have no header and start the data listing at the very first line)

The csv files delimiters must be comas (',')
========================================================================================================================