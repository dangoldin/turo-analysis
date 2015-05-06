#! /usr/bin/python

import sys

from relayrides import analyze_file
from edmunds import get_average_price

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Need to specify JSON'
        exit()
    listings = analyze_file(sys.argv[1])
    with open('out.csv', 'w') as f:
        f.write("make,model,year,rate,reviews,price\n")
        for l in listings:
            avg_price = get_average_price(l.make, l.model, l.year)
            print l,'=>', avg_price
            f.write("{0},{1},{2},{3},{4},{5}\n".format(l.make, l.model, l.year, l.rate, l.reviews, avg_price))
