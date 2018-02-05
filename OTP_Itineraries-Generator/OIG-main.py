import urllib.request
import json
import sys
import os, glob
import csv
import errno
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
TRIP_DATE = '2018/04/02'

def find_files(path, extension = 'csv', min = 2):
    """
    Get all the file of a given extension (default is .csv) in a directory.
    Raises an OSError if less than min are find
    :param path: directory where the files are
    :param extension: extension of the files that needs to be find (without the point e.g. 'csv' and NOT '.csv')
    :param min: minimum number of files that needs to be find (if less raise OSError)
    :return: files with the given extension
    """
    os.chdir(path)  # go to the directory of the path
    files = [i for i in glob.glob('*.{}'.format(extension))]  # place all the csv files in this array

    if len(files) < min:
        raise OSError("Couldn't find at least " + str(min) + " " + extension + " file(s)")

    return files


def create_od(csv_files):
    """
    Create python dict object that holds the data from the given origin/destination csv files
    :param csv_files: the files containing the OD data (2 or 3 csv files are needed in a specific format explained in the README)
    :return: dicts that contains the files data
    """
    ori = dict()
    des = dict()
    hredep = dict()
    ids = []
    tmp = []

    print("======================================================")
    print("= Extracting Origin/Destionation data from csv files =")
    print("======================================================")

    for file in csv_files:
        with open(file, 'r', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            if file.__contains__('ori'):  # file name needs to contain 'ori'

                print("     ===============")
                print("     = Origin file =")
                print("     ===============")
                i = 0

                numline = sum(1 for line in csvfile) - 1

                csvfile.seek(0)
                iter_spamreader = iter(spamreader)
                next(iter_spamreader)  # skip title row
                for row in iter_spamreader:
                    id = row[0]

                    ids.append(id)  # used to add an id to hredep if not already included in hours csv file

                    lon = row[1]
                    lat = row[2]
                    ori[id] = (lon, lat)
                    printrp('     ( ' + str(i) + ' / ' + str(numline) + ' )') if found_CmdPrinter else print(i)
                    i+=1
                print('     ( ' + str(i) + ' / ' + str(numline) + ' )')

            if file.__contains__('des'):  # file name needs to contain 'des'

                numline = sum(1 for line in csvfile) - 1

                print("     ====================")
                print("     = Destination file =")
                print("     ====================")
                i = 0

                csvfile.seek(0)
                iter_spamreader = iter(spamreader)
                next(iter_spamreader)  # skip title row
                for row in spamreader:
                    id = row[0]
                    lon = row[1]
                    lat = row[2]
                    des[id] = (lon, lat)
                    printrp('     ( ' + str(i) + ' / ' + str(numline) + ' )') if found_CmdPrinter else print(i)
                    i += 1
                print('     ( ' + str(i) + ' / ' + str(numline) + ' )')
            if file.__contains__('h'):
                for row in spamreader:
                    tmp.append(row)  # do later to make sure that the default ids are set

    i = 0
    # hours file
    ## note that if no hours file is given, the loop will not take place (since len(tmp) would be 0)
    if tmp:
        print("     ==============")
        print("     = Hours file =")
        print("     ==============")
    for row in tmp:
        if len(row) < 3:
            id = ids[i]
            hour = row[0]
            minute = row[1]
        elif len(row) == 3:
            id = row[0]
            hour = row[1]
            minute = row[2]
        hredep[id] = (hour, minute)
        i += 1
        printrp('     ( ' + str(i) + ' / ' + str(len(tmp)) + ' )') if found_CmdPrinter else print(i)
    print('     ( ' + str(i) + ' / ' + str(len(tmp)) + ' )')

    return ori, des, hredep

def download_json_files(ori, des, hredep=[]):
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
            url = build_url(ori[id][0], ori[id][1], des[id][0], des[id][1], hredep[id][0], hredep[id][1])
            extract_json(url, id, make_dir("OIG_jsonResults"))

            printrp('( ' + str(i) + ' / ' + str(len(ori)) + ' )') if found_CmdPrinter else print(i)
            i += 1

    print('( ' + str(i) + ' / ' + str(len(ori)) + ' )')


def build_url(ori_lon, ori_lat, des_lon, des_lat, hour='8', minute='00'):
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
    with open(FILE_OPTION_NAME, 'r', newline='') as file:
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
    time = hour + ':' + minute + ':00'

    url = 'http://' + base_URL + '?fromPlace=' + fromPlace + '&toPlace=' + toPlace + '&date=' + TRIP_DATE + '&time=' + time
    for option_name in options.keys():
        option = options[option_name]
        url += '&' + option_name + '=' + option
    if not 'mode' in url:
        url += '&mode=TRANSIT,WALK'

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
        raise OSError("Couldn't extract data from URL.  Make sure OTP server is running on the given server port")


def get_json_files_data(path, min = 1):
    """
    Get all the file of a given extension (default is .csv) in a directory.
    Raises an OSError if less than min are find
    :param path: directory where the files are
    :param min: minimum number of files that needs to be find (if less raise OSError)
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
    csv_output_path = make_dir("OIG_csvResults")

    if csv_output_file.split('.')[-1] != 'csv':
        raise OSError("File name must end with '.csv'")

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
        raise PermissionError('The file might be used by another app.')
    print('( ' + str(j-1) + ' / ' + str(len(full_data) - 1) + ' )')

def get_perceived_time(walkTime, transitTime, waitingTime):
    return (walkTime * PERCEIVED_WALK_FACTOR) + (transitTime * PERCEIVED_TRANSIT_FACTOR) + (waitingTime * PERCEIVED_WAIT_FACTOR)


## Test URL :
## http://localhost:8080/otp/routers/default/plan?fromPlace=48.40915,-71.04996&toPlace=48.41428,-71.06996&date=2017/12/04&time=8:00:00&mode=TRANSIT,WALK

## URL for isochrone ? maybe ? downloads a .zip file that contains god knows what
## localhost:8080/otp/routers/default/isochrone?layers=traveltime&styles=mask&batch=true&fromPlace=48.428766,-71.067439&date=2017/12/04&time=10:00:00&mode=TRANSIT&walkSpeed=3&maxWalkDistance=1000&precisionMeters=5000&cutoffSec=6900

## Given parameters :
# 1. path where the OD files are located
# 2. (Optional) Server port running OTP
# 3. (Optional) 'false' if we don't wan to download the json files

path = sys.argv[1] ## to be able to give the path as an argument in command line

download_json = True # set to False if the wanted JSON files are already downloaded on the computer
# TODO : remove this?

try:
    port = int(sys.argv[2]) # the server port can be given as argument, default is 8080
except IndexError:
    port = '8080'
except ValueError:
    download_json = sys.argv[2] != 'false'

try:
    # this raise an IndexError unless both the server port and the download_json arguments are given
    download_json = sys.argv[3] != 'false'
except IndexError:
    pass

extension = 'csv'

ret_dir = os.getcwd() # current directory to return to later

csv_files = find_files(path, extension, 2)
ori, des, hredep = create_od(csv_files)

os.chdir(ret_dir) # return to local directory

download_json_files(ori, des, hredep)

data = get_json_files_data('OIG_jsonResults')

os.chdir(ret_dir)

write_csv_file('data_scenario5.csv', data)


