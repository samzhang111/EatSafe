from math import radians, cos, sin, asin, sqrt
import urllib
import requests
from simplejson import JSONDecodeError
from settings import gkey, ykey

#google API query
gquery="https://maps.googleapis.com/maps/api/place/textsearch/json?query={q}&key=" + gkey
#yelp API query
yquery = 'http://api.yelp.com/business_review_search?term={name}&location={addr}&limit=1&ywsid=' + ykey

#============================================================================
# haversine
# 
# calculates geographical distance between two locations
#
# from http://stackoverflow.com/a/4913653/2907617
#
# variables:
#   - lon1, lat1 : long/lat coordinates of first point
#   - lon2, lat2 : long/lat coordinates of second point
#   
# returns:
#   distance between them, in meters
##===========================================================================

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    Returns answer in m
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    m = 6367 * c * 1000
    return m

def get_rating(score):
    if score < 43:
        rating = 'F'
    elif score < 66:
        rating = 'C'
    elif score < 96:
        rating = 'B'
    else:
        rating = 'A'

    return rating

#============================================================================
# get_geo:
# 
# Get long,lat from a query string q that mashes institution and address.
# For example: q="McDonald's near 525 S State St, Chicago IL"
# 
# Returns the Yelp id of the first restaurant that fulfills that quality
#
# Because of our love of Yelp ratings, and Yelp API's inability to do 
# fuzzy matching, we first query Google Places API to get the Name + Address.
#============================================================================
def get_geo(q):
    gq = gquery.format(q=urllib.quote_plus(q + ',Chicago,IL'))
    
    try:
        r = requests.get(gq)
    except requests.ConnectionError:
        print "Uh... hackathon. ConnectionError--check your wifi?"
        return

    if not r.ok:
        print "Request to Google API failed: {}.".format(r.code)
        return
    
    try:
        j = r.json()
    except JSONDecodeError:
        print r.text
        return
    
    if j and j['results']:
        item = j['results'][0]
        return {
                'lat': item['geometry']['location']['lat'],
                'long': item['geometry']['location']['lng']
                }

#============================================================================
# get_yelp_id:
# 
# Get yelp_id from a query string q that mashes institution and address.
# For example: q="McDonald's near 525 S State St, Chicago IL"
# 
# Returns the Yelp id of the first restaurant that fulfills that quality
#
# Because of our love of Yelp ratings, and Yelp API's inability to do 
# fuzzy matching, we first query Google Places API to get the Name + Address.
#============================================================================

def get_yelp_json(q, longitude=None,latitude=None):

    if longitude and latitude:
        loc = ',location={lat},{lng}'.format(
                lat=latitude,
                lng=longitude)
    else:
        loc = ', Chicago, IL'
    gq = gquery.format(q=urllib.quote_plus(q + loc))
    
    try:
        r = requests.get(gq)
    except requests.ConnectionError:
        print "Uh... hackathon. ConnectionError--check your wifi?"
        return

    if not r.ok:
        print "Request to Google API failed: {}.".format(r.code)
        return
    
    try:
        j = r.json()
    except JSONDecodeError:
        print r.text
        return
    
    try:
        name = j['results'][0]['name']
        addr = j['results'][0]['formatted_address']
    except KeyError:
        print "Key not found in get_yelp_id"
    except IndexError:
        print "Index out of range in get_yelp_id"
        return

#============================================================================
# Then, using that information, we query the Yelp API to get the Yelp ID
##===========================================================================
    
    yq = yquery.format(
            name=urllib.quote_plus(name.encode('utf-8')),
            addr=urllib.quote_plus(addr))
    try:
        r = requests.get(yq)
    except requests.ConnectionError:
        print "Uh... hackathon. ConnectionError--check your wifi?"
        return
    
    if not r.ok:
        print "Request to Yelp API failed: {}.".format(r.code)
        return
    
    try:
        yj = r.json()['businesses'][0]
    except IndexError:
        print "Bad Yelp API response!: " + r.text
        return
    
    return j['results'][0], yj
