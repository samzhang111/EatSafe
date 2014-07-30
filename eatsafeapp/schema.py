from eatsafeapp import eatsafeapp
from database import db
#from sqlalchemy import db.Column, Integer, Float, String, Date

class Inspection(db.Model):
    __tablename__ = 'food_inspections'
    Inspection_ID = db.Column(db.Integer, primary_key=True)
    DBA_Name = db.Column(db.String)
    AKA_Name = db.Column(db.String)
    License_No = db.Column(db.Integer)
    Facility_Type = db.Column(db.String)
    Risk = db.Column(db.String)
    Address = db.Column(db.String)
    City = db.Column(db.String)
    State = db.Column(db.String)
    Zip = db.Column(db.Integer)
    Inspection_Date = db.Column(db.String)
    Inspection_Type = db.Column(db.String)
    Results = db.Column(db.String)
    Violations = db.Column(db.String)
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Location = db.Column(db.String)
    Bankrupt = db.Column(db.Integer)
    Complaint = db.Column(db.Integer)
    Failure = db.Column(db.Integer)
    NoEntry = db.Column(db.Integer)
    ResultsNum = db.Column(db.Float)
    RestaurantID = db.Column(db.Integer)

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    #__searchable__ = ['db_name', 'db_addr', 
    #        'google_name', 'yelp_name', 'yelp_address']
    db_name = db.Column(db.String)
    db_addr = db.Column(db.String)
    
    google_id = db.Column(db.String)
    google_lat = db.Column(db.String)
    google_lng = db.Column(db.String)
    google_name = db.Column(db.String)
    google_price = db.Column(db.String)
    google_rating = db.Column(db.String)
    google_vicinity = db.Column(db.String)
 
    yelp_address = db.Column(db.String)
    yelp_id = db.Column(db.String)
    yelp_name = db.Column(db.String)
    yelp_phone = db.Column(db.String)
    yelp_photo_url = db.Column(db.String)
    yelp_rating = db.Column(db.String)
    yelp_rating_img_url = db.Column(db.String)
    yelp_review_count = db.Column(db.String)
    yelp_zip = db.Column(db.String)

    rating = db.Column(db.Float)
    num = db.Column(db.Integer)
    bankrupt = db.Column(db.Integer)
    complaints = db.Column(db.Integer)
    failures = db.Column(db.Integer)

    db_lat = db.Column(db.Float)
    db_long = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, primary_key=True)
    no_recent_fails = db.Column(db.Integer)
