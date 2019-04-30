import urllib.request
import json
import sys
import os, glob
import csv
import errno
import argparse
import math
from time import gmtime, strftime
try:
    # We want the script to run even if we don't have a CmdPrinter
    from CmdPrinter import printrp
    found_CmdPrinter = True
except ModuleNotFoundError:
    found_CmdPrinter = False

try :
    # We want the script to run even if we don't have a Timer
    import Timer
except ModuleNotFoundError:
    pass

import time


#################################################
# NEED AN OTP SERVER RUNNING TO RUN THIS SCRIPT #
#################################################


PERCEIVED_WALK_FACTOR = 1.5
PERCEIVED_WAIT_FACTOR = 2
PERCEIVED_TRANSIT_FACTOR = 1.25
FILE_OPTION_NAME = 'OIG_options.txt'
DEFAULT_OUTPUT = 'trips_data['+strftime("%Y%m%d%H%M%S", gmtime())+'].csv'
DEFAULT_JSON_OUTPUT = 'OIG_jsonResults['+strftime("%Y%m%d%H%M%S", gmtime())+']'
DEFAULT_PORT = '8080'
DEFAULT_YEAR = '2017'
DEFAULT_MONTH = '12'
DEFAULT_DAY = '04'
DEFAULT_HOUR = '8'
DEFAULT_MINUTE = '00'

def find_files(path, extension = 'csv', min = 2):
    """
    Get all the file of a given extension (default is .csv) in a directory.
    Error if less than min are find
    :param path: directory where the files are
    :param extension: extension of the files that needs to be find (without the point e.g. 'csv' and NOT '.csv')
    :param min: minimum number of files that needs to be find (if less Error)
    :return: files with the given extension
    """
    os.chdir(path)  # go to the directory of the path
    files = [i for i in glob.glob('*.{}'.format(extension))]  # place all the csv files in this array

    if len(files) < min:
        print("ERROR - Couldn't find at least " + str(min) + " " + extension + " file(s)")
        exit()

    return files

def verify_file_extension(path, extension = 'csv'):
    return path[-len(extension):] == extension;



def create_od_single_file(od_survey):
    ori = dict()
    des = dict()
    hredep = dict()
    date = dict()
    args = dict() # to store non-classic parameters (such as age, sex, salary, etc.)

    print("======================================================")
    print("= Extracting Origin/Destionation data from csv files =")
    print("======================================================")


    with open(od_survey, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0

        numline = sum(1 for line in csvfile) - 1

        csvfile.seek(0)
        for row in reader:
            try :
                orilon = row['orilon']
                orilat = row['orilat']
                ori[i] = {'orilon':orilon, 'orilat':orilat}
                deslon = row['deslon']
                deslat = row['deslat']
                des[i] = {'deslon':deslon, 'deslat':deslat}
            except KeyError:
                print("ERROR - Missing Origin/Destination coordinates.  "
                               "Make sure the headers for OD coordinates are 'orilon', 'orilat', 'deslon', 'deslat'")

            try :
                year = row['year']
            except KeyError:
                if verbose:
                    print("WARN - Line ", i, " : No column 'year' found.  Used default ", DEFAULT_YEAR)
                year = DEFAULT_YEAR

            try :
                month = row['month']
            except KeyError:
                if verbose:
                    print("WARN - Line ", i, " : No column 'month' found.  Used default ", DEFAULT_MONTH)
                month = DEFAULT_MONTH

            try :
                day = row['day']
            except KeyError:
                if verbose:
                    print("WARN - Line ", i, " : No column 'day' found.  Used default ", DEFAULT_DAY)
                day = DEFAULT_DAY

            date[i] = {'year':year, 'month':month, 'day':day}

            try:
                hour = row['hour']
            except KeyError:
                if verbose:
                    print("WARN - Line ", i, " : No column 'hour' found.  Used default ", DEFAULT_HOUR)
                hour = DEFAULT_HOUR

            try:
                minute = row['minute']
            except KeyError:
                if verbose:
                    print("WARN - Line ", i, " : No column 'minute' found.  Used default ", DEFAULT_MINUTE)
                minute = DEFAULT_MINUTE

            hredep[i] = {'hour':hour, 'minute':minute}


            tmp_args = dict()
            for column in row.keys():
                if column != 'orilon' and column !='orilat' and column !='deslon' \
                        and column !='deslat' and column !='year' and column !='month' \
                        and column !='day' and column !='hour' and column !='minute':
                    tmp_args[column] = row[column]
            args[i] = tmp_args
            i += 1
            printrp('( ' + str(i) + ' / ' + str(numline) + ' )') if found_CmdPrinter else print(i)

        print('( ' + str(i) + ' / ' + str(numline) + ' )')

    return ori, des, date, hredep, args


def download_json_files(ori, des, date, hredep, args):
    """
    Wrapper method to clean the code.
    Calls all the methods needed to download the JSON files from OTP API
    :param ori: origin file
    :param des: destination file
    :param hredep: (Optional) hours file
    :return:
    """

    print("======================================")
    print("= Extracting JSON files from OTP API =")
    print("======================================")
    i = 0
    for id in ori.keys():  # just so we can get all the ids (could have been des.keys() or hredep.keys())
        if download_json:
            # don't retrieve the data from OTP API if the user specifies it
            url = build_url(ori[id]['orilon'], ori[id]['orilat'],
                            des[id]['deslon'], des[id]['deslat'],
                            date[id]['year'], date[id]['month'], date[id]['day'],
                            hredep[id]['hour'], hredep[id]['minute'],
                            args[id])
            try :
                extract_json(url, id, make_dir(json_output))
            except OSError:
                print("ERROR : OTP is not currently running on the given port")
                exit();

            printrp('( ' + str(i) + ' / ' + str(len(ori)) + ' )') if found_CmdPrinter else print(i)
            i += 1
    if download_json:
        print('( ' + str(i) + ' / ' + str(len(ori)) + ' )')
    else:
        print("Already downloaded")


def build_url(ori_lon, ori_lat, des_lon, des_lat, year, month, day, hour, minute, args={}):
    """
    Build the URL from which the data will be retrieve.
    This is where we take into account the options in the Options txt file
    :param ori_lon: Longitude of the origin point
    :param ori_lat: Latitude of the origin point
    :param des_lon: Longitude of the destination point
    :param des_lat: Latitude of the destination point
    :param hour: (Optional) Hour of the departure (without the minutes) ie. For 12:35, put 12 for this param
    :param minute: (Optional) Minutes of the departure ie. For 12:35, put 35 for this param
    :return: The URL from from where the data can be retrieved
    """
    options = dict()
    with open(option_file, 'r', newline='') as file:
        # Read the options file
        for line in file:
            if line[0] == '#': # if the first character of a line is '#' skip it
                continue
            splited_line = line.rstrip().split(':')
            if len(splited_line) < 2: # if it is a line with no ':'
                continue
            options[splited_line[0]] = splited_line[1]
    base_URL = 'localhost:' + port + '/otp/routers/default/plan'
    fromPlace = ori_lon + ',' + ori_lat
    toPlace = des_lon + ',' + des_lat
    date = year + '/' + month + '/' + day
    time = hour + ':' + minute + ':00'

    url = 'http://' + base_URL + '?fromPlace=' + fromPlace + '&toPlace=' + toPlace + '&date=' + date + '&time=' + time
    for option_name in options.keys():
        option = options[option_name]
        url += '&' + option_name + '=' + option
    if not 'mode' in url:
        url += '&mode=TRANSIT,WALK'
    for key in args.keys():
        url+= '&' + key + '=' + args[key]

    return url


def extract_json(url, tripID, output_path):
    """
    Extract JSON file from a given URL, store it in a unique file
    :param url: URL from which to retrieve the data
    :return: data extracted from the URL as a python object (ie. dict)
    """
    testfile = urllib.request.URLopener()
    file_name = str(tripID) + ".json"

    try :
        testfile.retrieve(url, output_path + "\\" + file_name)  # place URL json file into a local json file
    except OSError:
        print("ERROR - Couldn't extract data from URL.  Make sure OTP server is running on the given server port")
        exit()


def get_json_files_data(path, min = 1):
    """
    Get all the file of a given extension (default is .csv) in a directory.
    Error if less than min are find
    :param path: directory where the files are
    :param min: minimum number of files that needs to be find (if less Error)
    :return: files with the given extension
    """

    json_files = find_files(path, "json", min)
    json_data = dict()

    print("===========================================")
    print("= Converting JSON data into Python object =")
    print("===========================================")
    i = 0
    for file in json_files:
        base = os.path.basename(file) # name with extension (ex. 'file.json')
        id = os.path.splitext(base)[0] # name without extension (ex. 'file') in this case, the names are the trip ids
        json_data[id] = json.load(open(file))  # get the json data as a python dict
        printrp('( ' + str(i) + ' / ' + str(len(json_files) - 1) + ' )') if found_CmdPrinter else print(i)
        i += 1

    print('( ' + str(i-1) + ' / ' + str(len(json_files) - 1) + ' )')
    return json_data


def make_dir(name='results'):
    """
    Make a folder in the current directory
    :param name: name of the created folder (default is 'results')
    :return: path of the newly created directory
    """
    output_path = os.getcwd() + '\\' + name
    directory = os.path.dirname(output_path + '\\toto')  # doesn't work w/o 'toto'
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return output_path


def write_csv_file(csv_output_file, full_data):
    """
    Write information in a csv file
    :param csv_output_file: name of the write-to file (will be create if doesn't already exist and overwrite if it does)(name must end with .csv)
    :param full_data: data of the json files as python object data[id] = dict() contaning one json file information
    :return:
    """
    j = 0
    csv_output_path = make_dir('OIG_csvResults')

    csv_file_path = csv_output_path + '\\' + csv_output_file

    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['tripId', 'agency_tripId', 'itinerary_nb', 'modes', 'actual_time', 'perceived_time',
                                'start_time', 'end_time', 'walk_time', 'walk_distance','transit_time', 'waiting_time',
                                'boardings', 'bus_lines_numbers', 'boarding_stop_ids', 'debarquer_stop_ids'])
            print("======================================")
            print("= Creating CSV file from JSON files  =")
            print("======================================")
            for id in full_data.keys():  # just so we can get all the ids
                data = full_data[id]
                j += 1

                printrp('( ' + str(j) + ' / ' + str(len(full_data) - 1) + ' )') if found_CmdPrinter else print(j)

                if 'error' in data:
                    # if no itineraries were find (ie. there was an error), write the error id and error message
                    # note : msg is the short message (eg. PATH_NOT_FOUND), message is the long description
                    csvwriter.writerow([id] + ['error'] + [str(data['error']['id'])] +
                                       [str(data['error']['message'])] + [str(data['error']['msg'])])
                else:
                    for itinerary_nb in range(len(data['plan']['itineraries'])):

                        boarding = 0
                        busNbs = ""
                        boarding_stop_ids = ""
                        debarquer_stop_ids = ""
                        agency_trip_ids = ""
                        modes = ""
                        for leg in data['plan']['itineraries'][itinerary_nb]['legs']:
                            modes += leg['mode'] + ';'
                            if leg['mode'] == 'BUS':
                                # every time a BUS step is included in the itineraries :
                                # add 1 to the boarding counter
                                # add the bus line number to busNbs
                                # add the stop_ids to boarding_stop_ids and debarquer_stop_ids
                                boarding += 1
                                busNbs += leg['route'] + ";"

                                boarding_stop_ids += str(leg['from']['stopCode']) + ';'
                                debarquer_stop_ids += str(leg['to']['stopCode']) + ';'
                                agency_trip_ids += str(leg['tripId'].split(':')[1]) + ';'
                                # we need to .split that line because tripId is given as agencyId:tripId


                        busNbs = busNbs[:-1]  # removing the trailing semi-colon
                        boarding_stop_ids = boarding_stop_ids[:-1]
                        debarquer_stop_ids = debarquer_stop_ids[:-1]
                        agency_trip_ids = agency_trip_ids[:-1]
                        modes = modes[:-1]
                        startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['plan']['itineraries'][itinerary_nb]['startTime']/1000))
                        endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['plan']['itineraries'][itinerary_nb]['endTime']/1000))
                        # those are /1000 because OTP gives Epoch time in milliseconds

                        walkTime = data['plan']['itineraries'][itinerary_nb]['walkTime']
                        transitTime = data['plan']['itineraries'][itinerary_nb]['transitTime']
                        waitingTime = data['plan']['itineraries'][itinerary_nb]['waitingTime']

                        # Write all the information inside a csv file
                        csvwriter.writerow([id,
                                            str(agency_trip_ids),
                                            str(itinerary_nb+1),
                                            str(modes),
                                            str(data['plan']['itineraries'][itinerary_nb]['duration']),
                                            str(get_perceived_time(walkTime, transitTime, waitingTime)),
                                            str(startTime),
                                            str(endTime),
                                            str(walkTime),
                                            str(data['plan']['itineraries'][itinerary_nb]['walkDistance']),
                                            str(transitTime),
                                            str(waitingTime),
                                            str(boarding),
                                            str(busNbs),
                                            str(boarding_stop_ids),
                                            str(debarquer_stop_ids)])
    except PermissionError:
        print('ERROR - Cannot write to CSV file.  The file might be used by another app.')
        exit()
    print('( ' + str(j-1) + ' / ' + str(len(full_data) - 1) + ' )')

def get_perceived_time(walkTime, transitTime, waitingTime):
    return (walkTime * PERCEIVED_WALK_FACTOR) + (transitTime * PERCEIVED_TRANSIT_FACTOR) + (waitingTime * PERCEIVED_WAIT_FACTOR)

def define_args():
    parser = argparse.ArgumentParser(description="This scripts takes in input an origin/destination csv file and outputs a csv files with the trips information")
    parser.add_argument('od_path', nargs='?',
                        help='Path to the OD file')
    parser.add_argument('--port', nargs="?",
                        help='Port on which OTP is currently running')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help="Increase output verbosity")
    parser.add_argument('--csv-output', dest='output', nargs="?",
                        help="Name of the outputed CSV file (will still be in the OIG_csvResults directory) (default : " + DEFAULT_OUTPUT + ')')
    parser.add_argument('--json-output', dest='json_output', nargs="?",
                        help="Name of the directory for the outputed JSON files (default : " + DEFAULT_OUTPUT + ')')
    parser.add_argument('--option-file', dest='option_file', nargs="?",
                        help="Path to the option txt file (default : " + FILE_OPTION_NAME + ')')
    parser.add_argument('--download', dest='download_json', action='store_true',
                        help="If the json data should be downloaded")
    parser.add_argument('--no-download', dest='download_json', action='store_false',
                        help="If the json data should not be downloaded (for this to work, there needs to be predownloaded json data in the OIG_jsonResults directory)")
    parser.set_defaults(download_json=True)
    parser.set_defaults(verbose=False)
    parser.set_defaults(output=DEFAULT_OUTPUT)
    parser.set_defaults(json_output=DEFAULT_JSON_OUTPUT)
    parser.set_defaults(option_file=FILE_OPTION_NAME)

    return parser.parse_args()

## Test URL :
## http://localhost:8080/otp/routers/default/plan?fromPlace=48.40915,-71.04996&toPlace=48.41428,-71.06996&date=2017/12/04&time=8:00:00&mode=TRANSIT,WALK

## URL for isochrone ? maybe ? downloads a .zip file that contains god knows what
## localhost:8080/otp/routers/default/isochrone?layers=traveltime&styles=mask&batch=true&fromPlace=48.428766,-71.067439&date=2017/12/04&time=10:00:00&mode=TRANSIT&walkSpeed=3&maxWalkDistance=1000&precisionMeters=5000&cutoffSec=6900

## Given parameters :
# 1. path where the OD file is located
# 2. (Optional) Server port running OTP
# 3. (Optional) 'false' if we don't want to download the json files

path = sys.argv[1] ## to be able to give the path as an argument in command line


args = define_args();
verbose = args.verbose
try :
    float(args.port)
    port = args.port
except ValueError :
    port = DEFAULT_PORT
    if verbose:
        print('Invalid port, using default : ', DEFAULT_PORT)
except TypeError :
    port = DEFAULT_PORT
    if verbose:
        print('Using default port : ', DEFAULT_PORT)

download_json = args.download_json
if download_json:
    json_output = args.json_output
    for dirpath, dirnames, files in os.walk(json_output):
        if files:
            print(dirpath, 'has files')
        if not files:
            print(dirpath, 'is empty')


csv_output = args.output
if csv_output.split('.')[-1] != 'csv':
    print("ERROR - Output file name must end with '.csv'")
    exit()
option_file = args.option_file
if option_file.split('.')[-1] != 'txt':
    print("ERROR - Option file name must end with '.txt'")
    exit()

extension = 'csv'

ret_dir = os.getcwd() # current directory to return to later

# csv_files = find_files(path, extension, 2)

if (verify_file_extension(path, extension)):
    #ori, des, hredep = create_od(path)
    ori, des, date, hredep, args = create_od_single_file(path)

    os.chdir(ret_dir) # return to local directory

    download_json_files(ori, des, date, hredep, args)

    data = get_json_files_data(json_output)

    os.chdir(ret_dir)

    write_csv_file(csv_output, data)
else :
    print("Error - Input file name must end with '.csv'")
    exit()
