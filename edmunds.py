#! /usr/bin/python

import requests
import json
import time
import random

from config import EDMUNDS_KEY, EDMNUDS_SECRET

MAX_ATTEMPTS = 6

SLEEP_BASE = 4
SLEEP_RAND = 3

# Increase our sleep time the fewer tries we have left
def smart_sleep(attempts_left, max_attempts):
    sleep_seconds = SLEEP_BASE + random.randint(0, SLEEP_RAND * (1 + MAX_ATTEMPTS - attempts_left))
    time.sleep(sleep_seconds)

def get_styles(make, model, year, attempts = MAX_ATTEMPTS):
    url = 'https://api.edmunds.com/api/vehicle/v2/{0}/{1}/{2}?fmt=json&api_key={3}'.format(make, model, year, EDMUNDS_KEY)
    r = requests.get(url)
    if r.status_code == 403 and attempts > 0: # Retry
        smart_sleep(attempts, MAX_ATTEMPTS)
        return get_styles(make, model, year, attempts - 1)
    if r.status_code != 200:
        print 'Status', r.status_code, r.content
        return {}
    else:
        return json.loads(r.content)

def get_price(style_id, attempts = MAX_ATTEMPTS):
    url = 'https://api.edmunds.com/v1/api/tmv/tmvservice/calculateusedtmv?styleid={0}&condition=Outstanding&mileage=25000&zip=07302&fmt=json&api_key={1}'.format(style_id, EDMUNDS_KEY)
    r = requests.get(url)
    if r.status_code == 403 and attempts > 0: # Retry
        smart_sleep(attempts, MAX_ATTEMPTS)
        return get_price(style_id, attempts - 1)
    if r.status_code != 200:
        print 'Status', r.status_code, r.content
        return {}
    else:
        return json.loads(r.content)

def get_average_price(make, model, year):
    try:
        styles = get_styles(make, model, year)
        # print json.dumps(styles, indent=2)
        prices = []
        for style in styles['styles']:
            style_id = style['id']
            # Pick arbitrary one for now
            price_info = get_price(style_id)
            try:
                price = price_info['tmv']['totalWithOptions']['usedPrivateParty']
            except Exception, e:
                print 'Error',e,price_info
                price = None
            if price and price > 0: # Skip bad records
                prices.append(price)
        if len(prices) > 0:
            return sum(prices)/(1.0 * len(prices))
        else:
            return None
    except Exception, e:
        print 'Failed to get price for {0}, {1}, {2}'.format(make, model, year)
        return None
