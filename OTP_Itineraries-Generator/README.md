## OTP_Itineraries-Generator

#### Please read the note at the bottom of this document

This scripts takes in input origin/destination csv file and outputs one json file per trip containing all the
data given by OTP as well as a csv files containing the following data :

- tripID,
- itinerary_nb, 
- duration,
- start_time, 
- end_time,
- walk_time, 
- walk_distance, 
- transit_time,
- waiting_time, 
- boardings, 
- bus_lines_numbers,
- boarding_stop_ids, 
- debarquer_stop_ids

The json files are placed in a directory called OIG_jsonResults itself placed at the project root
The csv file is placed in a directory called OIG_csvResults itself placed at the project root

A text file containing the trip options may be included in the OIG project directory.  Here's how to format it:

    - Any line starting with the character '#' will be skipped (as well as empty lines)
        
      Trip options must be written as 'option_name:value' with no space at any place in the line.
    option_name must be typed exactly as in the following list, otherwise it will have no effect.
      
        - The trip options are (each are explained in the given options file) :
      	    -   maxWalkDistance, 
              - maxHours, 
              - mode, 
              - numItineraries, 
              - walkSpeed, 
              - carSpeed,
              - walkReluctance, 
              - stairsReluctance, 
              - waitReluctance, 
              - waitAtBeginningFactor,  
              - ignoreRealtimeUpdates

Two optional file are contain in OTP_Itineraries-Generator, namely CmdPrinter and Timer.  The first one is a
pretty printer for the loading process and the second is a writes the Elapsed Time of the process at the end.
Both can be removed without causing any major problems.

The Elapsed Time of the project highly depends on the length of the OD files.

For other usages of the OTP api, here is a sample link for accessing itineraries data
http://localhost:8080/otp/routers/default/plan?fromPlace=48.40915,-71.04996&toPlace=48.41428,-71.06996&date=2017/12/04&time=8:00:00&mode=TRANSIT,WALK


## HOW TO RUN OTP_Itineraries-Generator

(1) Make sure python 3 is installed on your computer (tested with python 3.6.4)

(2) Start an instance of OpenTripPlanner
	(2.1) Direct to the directory containing the otp shaded.jar file
	(2.2) Type : `java -Xmx1G -jar otp-X.Y.Z-shaded.jar --build $LINK --inMemory  --port $PORT --securePort $S-PORT`
		(2.2.1) Where `otp-X.Y.Z-shaded.jar` is the otp shaded.jar name
		(2.2.2) `$LINK` is the directory containing the gtfs and osm files
		(2.2.3) Note that `-Xmx1G` represent the memory allocated to OTP, no less than 1G can be given
			and this parameter can be omitted (if so, OTP will have no memory limit)
		(2.2.4) The `--port` and `--securePort` can be omitted (default is 8080 and 8081).  If one is included, the other
		    MUST be too.  Note that `$PORT` and `$S-PORT` cannot point to the same port.
    For more detailed instructions, visit http://docs.opentripplanner.org/en/latest/Basic-Usage/

(3) Open a new terminal

(4) Direct into the directory containing the file named "OIG-main.py"

(5) Run OTP_Itineraries-Generator
```
	py OIG-main.py [-h] [--port [PORT]] [-v] [--csv-output [OUTPUT]]
                   [--json-output [JSON_OUTPUT]] [--option-file [OPTION_FILE]]
                   [--download] [--no-download]
                   [od_path]

	This scripts takes in input an origin/destination csv file and outputs a csv
	files with the trips information
	
	positional arguments:
  	  od_path               Path to the OD file

	optional arguments:
	  -h, --help            show this help message and exit
	  --port [PORT]         Port on which OTP is currently running
	  -v, --verbose         Increase output verbosity
	  --csv-output [OUTPUT]
	    	                Name of the outputed CSV file (will still be in the
	            	        OIG_csvResults directory) (default :
	                    	trips_data[20190430190152].csv)
	  --json-output [JSON_OUTPUT]
	    	                Name of the directory for the outputed JSON files
	            	        (default : trips_data[20190430190152].csv)
	  --option-file [OPTION_FILE]
	    	                Path to the option txt file (default :
	            	        OIG_options.txt)
	  --download            If the json data should be downloaded
	  --no-download         If the json data should not be downloaded (for this to
	    	                work, there needs to be predownloaded json data in the
	            	        OIG_jsonResults directory)
```



# IMPORTANT
The OD file needs to contain the followings :

NOTE : The columns need to be name EXACTLY the way they are written next (1 - 9)

At least these 4 columns:
   (1) orilon : longitude of the origin point
   (2) orilat : latitude of the origin point
   (3) deslon : longitude of the destination point
   (4) deslat : latitude of the destination point

And can contain the followings (these WILL affect the results if included) :
   (5) year : departure year from the origin point (default : 2018)
   (6) month : departure month from the origin point (default : 04)
   (7) day : departure day from the origin point (default : 02)
   (8) hour : departure hour from the origin point (default : 8)
   (9) minute : departure minute from the origin point (default : 00)

It can also contain any other information needed.  These will be in the request parameters but only for future reference (for statistic analysis and such), they WILL NOT affect the results.

The csv files delimiters must be comas (',')