#!/usr/bin/python


import argparse
import sys
import os
from datetime import datetime, timedelta
import glob

# exit 0 - OK
# exit 1 - WARNING
# exit 2 - CRITICAL
# exit 3 - UNKNOWN

def check_file(PATH, DAYS):
    # sanitaze user input:
    #PATH = arguments[0]
    #DAYS = arguments[1]

    # some sanity checks:

    # check is second argument is insteger
    try:
        DAYS_VAL = int(DAYS)
    except ValueError:
        print("UNKNOWN - Wrong number of days: %s" % DAYS)
        sys.exit(3)

    # check if file exists
    if not os.path.isfile(PATH):
        print("UNKNOWN - Path to file does not exist: %s" % PATH)
        sys.exit(3)

    OLDER_THAN = datetime.now() - timedelta(days=DAYS_VAL)
    FILETIME = datetime.fromtimestamp(os.path.getctime(PATH))

    if FILETIME < OLDER_THAN:
        print("CRITICAL - file %s older than %s days - backup broken!" % (PATH, DAYS))
        sys.exit(2)
    elif FILETIME == OLDER_THAN:
        print("WARNING - file %s has %s days - backup is broken?" % (PATH, DAYS))
        sys.exit(1)

    elif FILETIME > OLDER_THAN:
        print("OK - file %s has less than %s days - backup works OK" % (PATH, DAYS))
        sys.exit(0)
    else:
        print("UNKNOWN - error checking age of file %s !" % (PATH))
        sys.exit(3)


def check_dir(DIR, DAYS):
    # some sanity checks:

    # check is second argument is insteger

    # check if file exists
    if not os.path.isdir(DIR):
        print("CRITICAL - Path to directory does not exist: %s" % DIR)
        sys.exit(2)

    # check if directory is empty:
    if not os.listdir(DIR):
        print("CRITICAL - Directory %s is empty - backup broken!" % DIR)
        sys.exit(2)

    # get the latest file in directory
    LIST_OF_FILES = glob.glob(DIR + '/*')
    LATEST_FILE = max(LIST_OF_FILES, key=os.path.getctime)

    # check if this file is older than defined value:
    check_file(LATEST_FILE, DAYS)


parser=argparse.ArgumentParser(
            description='''Check if date of file creation is older than given number of days ''',
                epilog="""Designed by mkola for Icinga 2 monitoring.""")
parser.add_argument('--file', type=str, help='Path to file')
parser.add_argument('--days', type=str, help='Age of file: not older than this value')
parser.add_argument('--dir', type=str, help='Path to directory in which we should search for newest file')
args=parser.parse_args()

if not len(sys.argv) > 1:
    parser.print_help(sys.stderr)
    sys.exit(3)

if args.file and args.days:
    check_file(args.file, args.days)

if args.dir and args.days:
    check_dir(args.dir, args.days)

