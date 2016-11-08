#!/usr/bin/env python3
#
# Copyright 2016 Plantcubed
#

import argparse
import json
import uuid
from json import JSONEncoder
import inspect

convertlist = {}
_recipe_transfer =  list()

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class InvalidTimeString(Exception):
    pass

class FailedParse(Exception):
    pass

def commandLineInit():
    program_description = "convert old gro format to new\n"
    program_epilog = ("Note: If multiple logging flags are set, highest one will be chosen.\n"
                      "Default log level is logging.WARNING. --info is nice too."
                      )
    parser = argparse.ArgumentParser(description=program_description,
                                     epilog=program_epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', '--file', help='input file', default='')
    parser.add_argument('-d', '--desc', help='description', default='')

    args = parser.parse_args()
    args_dict = vars(args)
    return args_dict


def parse_command_line(line):
    try:
        # parse line for time stamp and command
        newcmd = line.strip()
        args = line.split(' ')
    except ValueError:
        raise FailedParse()

    try:
        comment_start = args.index('#')
        args = args[0:comment_start]
    except ValueError:
        pass

    return args


def parse_time_string(time_string):
    time_args = time_string.split(':')
    if len(time_args) != 4:
        raise InvalidTimeString()
    try:
        time_args = [int(arg) for arg in time_args]
    except ValueError:
        raise InvalidTimeString()
    return time_args.pop() + 60 * time_args.pop() + 60 * 60 * time_args.pop() + \
           60 * 60 * 24 * time_args.pop()


def loadconvertRecipeFile(filename):
    # load file, convert 000:00:00 to unix time reduce time needed during the run
    global _recipe_transfer

    with open(filename) as f:
        _recipe_temp = f.readlines()

    for line in _recipe_temp:
        if '#' in line:
            line = line[:line.index('#')]

        try:
            # parse line for time stamp and command
            myargs = parse_command_line(line)
        except FailedParse:
            #_recipe_transfer[count] = '#Error:Parse:' + line
            continue

        time_string = myargs.pop(0)
        try:
            timedelta = parse_time_string(time_string)
            #print(timedelta)
        except InvalidTimeString:
            #_recipe_transfer[count] = '#Error:TimeStamp:' + line
            continue

        # write everything back out
        str1 = ""
        str2 = ""
        try:
            str1 = myargs.pop(0)
            str2 = myargs.pop(0)
        except IndexError:
            pass

        command = convertlist[str1[:4]]
        if not 'done' in command:
            test = [ timedelta,command, float(str2) ]
            _recipe_transfer.append(test)

def writeNewFormat(filename, desciprion):
    global _recipe_transfer

    me = Object();
    tid = str(uuid.uuid4())
    tid = tid.replace('-','')

    me._id =  tid
    me.description = desciprion
    me.operations = _recipe_transfer

    fileout = open('new_' + filename, 'w+')
    fileout.write(me.toJSON())
    fileout.close()

def buildconvertlist():
    global convertlist
    convertlist['AACR'] = 'air_circulation_fan'
    convertlist['AWCR'] = 'water_circulation_pump'
    convertlist['AWAR'] = 'water_aeration_pump'
    convertlist['SLIN'] = 'light_illuminance'
    convertlist['SATM'] = 'air_temperature'
    convertlist['SAHU'] = 'air_humidity'
    convertlist['SACO'] = 'air_carbon_dioxide'
    convertlist['ALUV'] = 'ultraviolet_leds'
    convertlist['GHAR'] = 'done'

if __name__ == '__main__':
    # get filename from command line
    cmdargs_dict = commandLineInit()
    # built the converter list
    buildconvertlist()
    # load the file into _recipe_transfer and convert format
    loadconvertRecipeFile(cmdargs_dict['file'])
    # build new file
    writeNewFormat(cmdargs_dict['file'],cmdargs_dict['desc'])
    # we are done here


