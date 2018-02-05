import os
import glob
import csv
import sys
import json
import copy
try:
    import Timer
except ModuleNotFoundError:
    # We want the script to run even without a Timer
    pass

try :
    from CmdPrinter import printrp
    found_CmdPrinter = True
except ModuleNotFoundError:
    # Print differently whether or not we have a CmdPrinter
    found_CmdPrinter = False

def get_json_files_data(path, min = 1):
    """
    Get all the file of a given extension (default is .csv) in a directory.
    Raises an OSError if less than min are find
    :param path: directory where the files are
    :param min: minimum number of files that needs to be find (if less raise OSError)
    :return: files with the given extension
    """

    extension = ".json"

    json_pattern = os.path.join(path, '*.json') # set the pattern
    files = glob.glob(json_pattern) # get the .json files from path (format : path from root to file)

    if len(files) < min:
        # need at least two file (origin and destination) hours file is optional
        raise OSError("Couldn't find at least " + str(min) + " " + extension + " file(s)")

    json_data = dict()

    for file in files:
        base = os.path.basename(file) # name with extension (ex. 'file.json')
        id = os.path.splitext(base)[0] # name without extension (ex. 'file') in this case, the names are the trip ids
        json_data[id] = json.load(open(file))  # get the json data as a python dict

    return json_data


def write_csv_file(json_datas, attributes):
    """
    Write information from the json_data corresponding to the attributes in a csv file
    :param json_data: data from which to retrieve the information (expect to be a dict with tripIDs as keys and json data (in python dict) as value)
    :param attributes: array of attributes to retrieve from the json files (must be of format ["path/to/attribute", "path/to/other/attribute"]
    :return:
    """
    j = 0

    csv_output_file = 'results.csv'

    splited_attributes = []
    for attribute in attributes:
        splited_attributes += [attribute.split('/')]

    # Exemple of the above process:
    # Input : ['plan/itineraries/0/duration', 'requestParameters/date]
    # Output : [['plan','itineraries,'0','duration'], ['requestParameters','date']]

    with open(csv_output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')

        # write the header
        header = []
        for attribute in splited_attributes:
            header += [attribute[-1]] # attribute[-1] is the name of the attribute
            # TODO : Make the header more significant
        csvwriter.writerow(header)

        for id in json_datas.keys():
            data = json_datas[id]

            j += 1  # counter to keep track of the progress

            if found_CmdPrinter :
                # if we have a CmdPrinter, use this method
                printrp(str(j) + '...')
            else:
                print(j)

            if 'error' in data:
                # if no itineraries were find (ie. there was an error), write the error id and short error message
                csvwriter.writerow([id] + ['error'] + [str(data['error']['id'])] + [str(data['error']['message'])])
            else:

                row = []  # the next row that will be written in the csv file
                loop = False

                splited_attributes = adjust_path(splited_attributes, data)

                for attribute_path in splited_attributes:

                    # From the above exemple :
                    # splited_attibutes = [['plan','itineraries,'0','duration'], ['requestParameters','date']]
                    # attribute = ['plan','itineraries,'0','duration']

                    row += [find_attribute(attribute_path, data)]

                csvwriter.writerow(row)


def adjust_path(splited_attributes, data):

    # NOTE :
    # This method was stopped mid-proccess because of unexpected plan changes, the intent of this method was
    # to add path that correspond to all the itineraries/legs/steps of a tric
    # e.g. [plan,itineraries,legs,startTime] --> [[plan,itineraries,0,legs,0,startTime],
    #                                             [plan,itineraries,0,legs,1,startTime], ...
    #                                             [plan,itineraries,1,legs,0,startTime],...]

    tmp_data = copy.deepcopy(data)
    adjusted_attributes = []
    for attibute in splited_attributes:
        i = 0
        for branch in attibute:
            tmp_data = tmp_data[branch]
            if branch == 'itineraries' or 'steps' or 'legs':
                for j in range(len(tmp_data)):
                    adjusted_attributes += [attibute[:i+1] + [str(j)] + attibute[i+1:]]
            i += 1
        if 'itineraries' or 'legs' or 'steps' in attibute:
            pass
        else:
            adjusted_attributes += attibute

def find_attribute(attribute_path, data):
    """
    This recursive method finds an attribute from a path
    e.g. ['plan','itineraries','0','duration'] returns data['plan']['itineraries'][0]['duration'] = 1538 (dummy)
    :param attribute_path: array of string that describe the path to an element of the data dictionary
    :param data: json data as python object
    :return: the attribute corresponding to the given path
    """

    if len(attribute_path) == 1:
        return data[attribute_path[0]]

    for branch in attribute_path:


        try:
            # data is usually expected to be a dict, but can be an indexed list
            return find_attribute(attribute_path[1:], data[branch])
        except TypeError:
            # a TypeError only occurs when data is an indexed list (ie. integer index)
            # and not a dict as usual (ie. String index)
            return find_attribute(attribute_path[1:], data[int(branch)])

        # From the above exemple :
        # final return value is data['plan']['itineraries'][0]['duration'] = 1538 (dummy)

# For testing
json_files_path = r"C:\Users\olivi\Dropbox\Civilia\OTP_Attributes-Retriever\json_test"

#json_files_path = sys.argv[1]
#attributes = sys.argv[2].replace(';',',').split(',')

json_data = get_json_files_data(json_files_path)
write_csv_file(json_data, ["plan/itineraries/0/duration", "requestParameters/date","plan/from/lon"])

# TODO : Make a csv or txt file that holds shortcuts to path
# Exemple : fst_duration = plan/itineraries/0/duration