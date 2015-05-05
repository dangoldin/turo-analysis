#! /usr/bin/python

import requests
import json

from config import EDMUNDS_KEY, EDMNUDS_SECRET

def get_styles(make, model, year):
    url = 'https://api.edmunds.com/api/vehicle/v2/{0}/{1}/{2}?fmt=json&api_key={3}'.format(make, model, year, EDMUNDS_KEY)
    r = requests.get(url)
    if r.status_code != 200:
        return {}
    else:
        return json.dumps(r.content)

def get_price(make, model, year):
    styles = get_styles(make, model, year)
    print json.dumps(styles, indent=2)
