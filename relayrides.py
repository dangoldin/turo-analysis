#! /usr/bin/python

import sys
import requests
import urllib
import json

from collections import namedtuple

Listing = namedtuple('Listing', ['make', 'model', 'year', 'rate', 'reviews'])

def read_file(p):
    with open(p, 'r') as f:
        return json.loads(f.read())

def analyze_file(p):
    return analyze(read_file(p))

def analyze(j):
    print json.dumps(j, indent=2)

    print '# of cars: {0}'.format(len(j['list']))

    listings = []
    for l in j['list']:
        rate = l['rate']['daily']
        make = l['vehicle']['make']
        model = l['vehicle']['model']
        year = l['vehicle']['year']
        reviews = l['reviewCount']

        print ",".join(str(x) for x in [make, model, year, rate, reviews])

        l = Listing(make, model, year, rate, reviews)
        listings.append(l)
    return listings

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Need to specify JSON'
        exit()
    analyze_file(read_file(sys.argv[1]))

# curl 'https://relayrides.com/api/search?location=Jersey+City%2C+NJ%2C+USA&maximumDistanceInMiles=30&latitude=40.72815749999999&longitude=-74.0776417&cityName=&locality=Jersey+City%2C+NJ&locationType=City&page=1&itemsPerPage=2000&searchStrategyName=srv5f&_=1430707402658' -H 'Cookie: JSESSIONID=4075DEBD0BCAEE3B35CCC88BDF68F255; rr_u_cid=wVtF0xx-Tkqsgi7hIYDH5A; optimizelyEndUserId=oeu1430707372397r0.7057498847134411; __ssid=bf3d26d5-3297-490f-b1dc-9a07c159eb8e; _gat=1; km_ai=6grs45qWmdeTgLdA8Y20Y%2BgvKXI%3D; kvcd=1430707399466; km_vs=1; km_lv=1430707399; times=%7B%7D; airportCode=undefined; km_uq=; _ga=GA1.2.209873066.1430707376; optimizelySegments=%7B%22205581881%22%3A%22false%22%2C%22205592551%22%3A%22gc%22%2C%22205606556%22%3A%22campaign%22%7D; optimizelyBuckets=%7B%7D; optimizelyPendingLogEvents=%5B%5D; IRF_undefined=%7Bvisits%3A1%2Cuser%3A%7Btime%3A1430707372630%2Cref%3A%22https%3A//www.google.com/%22%2Cpv%3A7%2Ccap%3A%7B%7D%2Cv%3A%7B%7D%7D%2Cvisit%3A%7Btime%3A1430707372630%2Cref%3A%22https%3A//www.google.com/%22%2Cpv%3A7%2Ccap%3A%7B%7D%2Cv%3A%7B%7D%7D%2Clp%3A%22https%3A//relayrides.com/%22%2Cdebug%3A0%2Ca%3A1430707402511%7D; __ar_v4=ZYMPYGNPRZAEVMCIO7T4UW%3A20150503%3A6%7CU6FUA32JF5BGROBUOQCXVE%3A20150503%3A6%7CRMYOAUY6BBFQDGBG6YNC6S%3A20150503%3A5%7CFLZS2FVNMVCQNMBIV6NG4F%3A20150503%3A1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2385.0 Safari/537.36' -H 'Accept: */*' -H 'Referer: https://relayrides.com/search?location=Jersey+City%2C+NJ%2C+United+States&startDate=&endDate=' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed
