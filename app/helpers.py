from math import radians, cos, sin, asin, sqrt
import urllib
import requests
from simplejson import JSONDecodeError

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

