#! /usr/bin/python

import sys
import time

from relayrides import analyze_file
from edmunds import get_average_price
import concurrent.futures

def get_avg_price_row(l):
    time.sleep(1)
    avg_price = get_average_price(l.make, l.model, l.year)
    return "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(l.make, l.model, l.year, l.rate, l.rating, l.reviews, l.trips_taken, l.created, avg_price)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Need to specify JSON input'
        exit()
    try:
        outfile = sys.argv[2]
    except Exception, e:
        outfile = 'out.csv'
    listings = analyze_file(sys.argv[1])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        out_list = list( executor.map(get_avg_price_row, listings) )
    with open(outfile, 'w') as f:
        f.write("make,model,year,rate,rating,reviews,trips_taken,created,price\n")
        for l in out_list:
            print l,
            f.write(l)
