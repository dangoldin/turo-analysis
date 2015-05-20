#! /usr/bin/python

import sys
import time

from relayrides import analyze_file
from edmunds import get_average_price
import concurrent.futures
from datetime import datetime

def get_avg_price_row(l):
    time.sleep(1)
    avg_price = get_average_price(l.make, l.model, l.year)
    return (l, avg_price)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Need to specify JSON input'
        exit()
    try:
        outfile = sys.argv[2]
    except Exception, e:
        outfile = 'out.csv'
    today = datetime.now()
    listings = analyze_file(sys.argv[1])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        out_list = list( executor.map(get_avg_price_row, listings) )
    with open(outfile, 'w') as f:
        f.write("make,model,year,rate,rating,reviews,trips_taken,created,city,state,distance,price,days_listed,avg_trips_taken_per_day,avg_rate_per_day,price_vs_rate_per_day\n")
        for l, avg_price in out_list:
            days_listed = (today - l.created).days
            try:
                trips_taken_per_day = (1.0 * l.trips_taken)/days_listed
            except:
                trips_taken_per_day = None
            try:
                rate_per_day = trips_taken_per_day * l.rate
            except:
                rate_per_day = None
            try:
                price_vs_rate_per_day = avg_price/rate_per_day
            except:
                price_vs_rate_per_day = None
            print l, avg_price, days_listed, trips_taken_per_day, rate_per_day, price_vs_rate_per_day
            row = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}\n".format(
                l.make, l.model, l.year, l.rate, l.rating, l.reviews, l.trips_taken, l.created, l.city, l.state, l.distance,
                avg_price, days_listed, trips_taken_per_day, rate_per_day, price_vs_rate_per_day)
            f.write(row)
