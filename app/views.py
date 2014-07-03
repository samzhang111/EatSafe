from app import app
import flask
from flask import render_template
from flask import request
from flask import Response
from flask import abort

from simplejson import JSONDecodeError

import json
from database import session
from schema import Inspection, Restaurant
from math import radians, cos, sin, asin, sqrt
from sqlalchemy.sql import func
from helpers import haversine, get_rating, get_geo, get_yelp_json
import requests
import urllib
from settings import gkey, ykey

from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()
#google API query
gquery="https://maps.googleapis.com/maps/api/place/textsearch/json?query={q}&key={g}" 
#yelp API query
yquery = 'http://api.yelp.com/business_review_search?term={name}&location={addr}&limit=1&ywsid={y}'
#google instant API
ginstant = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={substring}&types=establishment&radius=500&location={lat},{lng}&key={g}'

default_photo = 'http://s3-media1.fl.yelpcdn.com/assets/2/www/img/5f69f303f17c/default_avatars/business_medium_square.png'

#============================================================================
# Failed attempt at creating a web version of the app
##===========================================================================
@app.route('/map')
def show_map():
    return render_template('map.html', key=gkey)

@app.route('/instant')
def instant():
    """
    /instant
     Google Places Autocomplete API endpoint
     Arguments: query -- query
                long  -- longitude
                lat   -- latitude 
           
    if long and lat are not provided, the center of Chicago is used
    """
    query = request.args.get('query', '', type=str)
    longitude = request.args.get('long', '-87.625916', type=str)
    latitude = request.args.get('lat', '41.903196', type=str)
    
    if not query or not longitude or not latitude:
        abort(400)
    
    gq = ginstant.format(substring=urllib.quote_plus(query),
            lat=latitude,
            lng=longitude,
            g=gkey
            )
 
    try:
        r = requests.get(gq)
    except requests.ConnectionError:
        abort(500)

    if not r.ok:
        abort(500)

    try:
        j = r.json()
    except JSONDecodeError:
        abort(500)
 
    all_restaurants_dict = get_restaurants_dict()

    result = []
    if j and j.has_key('predictions'):
        print j
        for pred in j['predictions']:
            try:
                item = all_restaurants_dict[pred['place_id']]
                result.append(item)
            except KeyError:
                continue
        
    return Response(json.dumps(result), mimetype='text/json')


@app.route('/place')
def place():
    """
    /place

     JSON API for retrieving detailed inspection information about a 
     particular establishment.

     Takes:
       - id  : the Google Places ID of the establishment

     returns:
    {
       "rating":"B",
       "yelp_review_count":"254",
       "pic":"http://media2.fl.yelpcdn.com/bpthumb/DY0j0ILnUgxib_e1Nqbn4Q/ms",
       "yelp_rating":"3.5",
       "phone":"3129292423",
       "inspections":[
          {
             "inspection_type":"Canvass Re-Inspection",
             "inspection_id":1199353,
             "inspection_date":"03-07-2014",
             "inspection_result":100
          },
          ...(repeat)
       ],
       "id":"ChIJA2ChzVHTD4gRPSWx89UMbOs",
       "addr":"12 E Cedar St",
       "count":11,
       "fails":3,
       "name":"Da Lobsta",
       "new":false
    }
    """ 

    google_id = request.args.get('id', '', type=str)
    
    if not google_id:
        abort(400)

    info = session.query(
        Restaurant.google_id,
        Restaurant.db_name,
        Restaurant.db_addr,
        Restaurant.google_name,
        Restaurant.google_lat,
        Restaurant.google_lng,
        Restaurant.yelp_name,
        Restaurant.yelp_rating,
        Restaurant.yelp_review_count,
        Restaurant.yelp_photo_url,
        Restaurant.yelp_rating_img_url,
        Restaurant.yelp_address,
        Restaurant.yelp_zip,
        Restaurant.yelp_phone,
        Restaurant.rating,
        Restaurant.complaints,
        Restaurant.db_long,
        Restaurant.db_lat,
        Restaurant.num,
        Restaurant.failures).filter(Restaurant.google_id==google_id).one()
    
    info_dict = info.__dict__

    inspection_cols = ['inspection_id',
            'inspection_date',
            'inspection_result',
            'inspection_type']
    inspection_keys = {x:i for i,x in enumerate(inspection_cols)}

    inspections = session.query(
            Inspection.Inspection_ID,
            Inspection.Inspection_Date,
            Inspection.Results,
            Inspection.Inspection_Type
            ).filter(
                    Inspection.AKA_Name==info_dict['db_name'] and
                    Inspection.Address==info_dict['db_addr']).all()

    name = info_dict['google_name'] or info_dict['db_name']
    addr = info_dict['yelp_address'] or info_dict['db_addr']
    photo = info_dict['yelp_photo_url'] or default_photo
    rating = get_rating(info_dict['rating'])
    new = info_dict['num'] <= 1
    
    inspections_dict = []
    for inspection in inspections:
        inspections_dict.append(dict(zip(inspection_cols, inspection)))


    returned = {
            'id': info_dict['google_id'],
            'name': name,
            'addr': addr,
            'pic': photo,
            'phone': info_dict['yelp_phone'],
            'rating': rating,
            'count': info_dict['num'],
            'fails': info_dict['failures'],
            'yelp_rating': info_dict['yelp_rating'],
            'yelp_review_count': info_dict['yelp_review_count'],
            'new': new,
            'inspections': inspections_dict
            }
    
    return Response(json.dumps(returned), mimetype='text/json')


@app.route('/near')
def check():
    """

    check():

     route /near?
     find nearby restaurants and their aggregate health inspection scores
     
     required variables:
     -long: the longitude to search near
     -lat: the latitude to search near

returns:
     {
     'name': name of the restaurant,
     'address': address,
     'google_id': google place ID--> use for if they click
     'dist': distance in miles,
     'pic': link to photo,
     'rating': letter rating (A, B, C, F, ?),
     'yelp_rating': yelp rating (float: 0, 0.5, ..., 3.5, 4)
     }
     
     a json string object of list of closest 20 restaurants and their health
     inspection scores
     
     note: distance is returned in miles

    """
    MAX_DIST = 5000
    longitude = request.args.get('long', '', type=float)
    latitude = request.args.get('lat', '', type=float)

    if not (longitude and latitude):
        abort(400)

    # get all unique restaurants from the database
    
    all_restaurants = get_restaurants()
    
    # loop through all restaurants, calculate distance
    valid = []
    results = []

    for row in all_restaurants:
        row = row.__dict__

        # throw away all restaurants without google IDs
        if not row['google_id']:
            continue
        
        # throw away restaurants without longitude
        if not row['db_long'] and not row['google_lng']:
            continue
        
        # use google stuff when we have it
        if row['google_lng']:
            lng, lat = map(float, 
                    (row['google_lng'], row['google_lat']))
        else:
            lng, lat = row['db_long'], row['db_lat']

        d = haversine(longitude, latitude, lng, lat)

        if d < MAX_DIST:
            row['d'] = d
            valid.append(row)

    closest = sorted(valid, key=lambda x: x['d'])[:20]
    
    for row in closest:
        addr = row['yelp_address'] or row['db_addr']
        photo = row['yelp_photo_url'] or default_photo
        
        rating = get_rating(row['rating'])
        new = row['num'] <= 1
        
        
        if row['d'] < 1609:
            miles = '%.2f'%(row['d']*0.000621371)
        else:
            miles = '%.1f'%(row['d']*0.000621371)
        
        results.append({
                'name': row['google_name'],
                'id': row['google_id'],
                'address': addr,
                'dist': miles,
                'pic': photo,
                'rating': rating,
                'yelp_rating': row['yelp_rating'],
                'new': new
            })
    

    # formulate json response
    return Response(json.dumps(results), mimetype='text/json')

@app.errorhandler(400)
def bad_request():
    return json.dumps({'error': 'bad API arguments'})

@app.errorhandler(500)
def bad_request():
    return json.dumps({'error': 'Internal Server Error'})

def get_restaurants():
    """
    get_restaurants()

    Returns a list of all the restaurants. Makes sure the list is cached.
    """
    all_restaurants = cache.get('all_restaurants')
    if not all_restaurants:
        all_restaurants = session.query(
            Restaurant.google_id,
            Restaurant.db_name,
            Restaurant.db_addr,
            Restaurant.google_name,
            Restaurant.google_lat,
            Restaurant.google_lng,
            Restaurant.yelp_name,
            Restaurant.yelp_rating,
            Restaurant.yelp_review_count,
            Restaurant.yelp_photo_url,
            Restaurant.yelp_rating_img_url,
            Restaurant.yelp_address,
            Restaurant.yelp_zip,
            Restaurant.yelp_phone,
            Restaurant.rating,
            Restaurant.complaints,
            Restaurant.db_long,
            Restaurant.db_lat,
            Restaurant.num).all()
        cache.set('all_restaurants', all_restaurants, timeout=24*60*60)
    return all_restaurants

def get_restaurants_dict():
    all_restaurants_dict = cache.get('all_restaurants_dict')
    if not all_restaurants_dict:
        restaurants = get_restaurants()
        all_restaurants_dict = {}
        for restaurant in restaurants:
            all_restaurants_dict[restaurant[0]] = restaurant.__dict__
    
        cache.set('all_restaurants_dict', all_restaurants_dict, timeout=24*60*60)
    return all_restaurants_dict
