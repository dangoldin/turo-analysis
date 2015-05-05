#! /usr/bin/python

import sys

from relayrides import analyze_file
from edmunds import get_price

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Need to specify JSON'
        exit()
    listings = analyze_file(sys.argv[1])
    for l in listings:
        print l
