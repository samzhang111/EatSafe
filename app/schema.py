from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date

Base = declarative_base()

class Inspection(Base):
    __tablename__ = 'food_inspections'
    Inspection_ID = Column(String, primary_key=True)
    DBA_Name = Column(String)
    AKA_Name = Column(String)
    License_No = Column(Integer)
    Facility_Type = Column(String)
    Risk = Column(String)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Zip = Column(Integer)
    Inspection_Date = Column(String)
    Inspection_Type = Column(String)
    Results = Column(String)
    Violations = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    Complaint = Column(Integer)
    Failure = Column(Integer)

class Restaurant(Base):
    __tablename__ = 'restaurants'
    google_id = Column(String, primary_key=True)
    db_name = Column(String)
    db_addr = Column(String)
    
    google_name = Column(String)
    google_vicinity = Column(String)
    google_rating = Column(String)
    google_price = Column(String)
    google_lat = Column(String)
    google_lng = Column(String)
 
    yelp_id = Column(String, primary_key=True)
    yelp_name = Column(String)
    yelp_rating = Column(Float)
    yelp_review_count = Column(Integer)
    yelp_photo_url = Column(String)
    yelp_rating_img_url = Column(String)
    yelp_address = Column(String)
    yelp_zip = Column(String)
    yelp_phone = Column(String)

    rating = Column(Float)
    num = Column(Integer)
    bankrupt = Column(Integer)
    complaints = Column(Integer)
    failures = Column(Integer)

    db_lat = Column(Float)
    db_long = Column(Float)
