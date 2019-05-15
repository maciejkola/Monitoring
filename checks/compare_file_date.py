#!/usr/bin/python


import argparse
import sys
import os
from datetime import datetime, timedelta

# exit 0 - OK
# exit 1 - WARNING
# exit 2 - CRITICAL
# exit 3 - UNKNOWN

def check(PATH, DAYS):
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




parser=argparse.ArgumentParser(
            description='''Check if date of file creation is older than given number of days ''',
                epilog="""Designed by mkola for Icinga 2 monitoring.""")
parser.add_argument('--path', type=str, help='Path to file')
parser.add_argument('--days', type=str, help='Age of file: not older than this value')
args=parser.parse_args()

if not len(sys.argv) > 1:
    parser.print_help(sys.stderr)
    sys.exit(3)

if args.path and args.days:
    check(args.path, args.days)
