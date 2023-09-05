from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///diner_tracker.db')  
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    health_rating = Column(Integer)

    inspections = relationship('Inspection', backref=backref('restaurant'))

class Inspection(Base):
    __tablename__ = 'inspections'

    id = Column(Integer(), primary_key=True)
    inspector = Column(Integer())
    date = Column(Date())
    # Define relationship
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))  
    # One to many relationship
    restaurant = relationship('Restaurant', backref=backref('inspections'))

    inspection_results = relationship('InspectionResult', backref=backref('inspection'))

class InspectionResult(Base):
    __tablename__ = 'inspection_results'

    id = Column(Integer(), primary_key=True)
    results = Column(String())
    inspection_id = Column(Integer(), ForeignKey('inspections.id'))

    inspection = relationship('Inspection', backref=backref('inspection_results'))

    print ('Hello ken')
