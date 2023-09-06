from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship
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

    inspections = relationship('Inspection', back_populates='restaurant')

    def __repr__(self):
        return f"<Restaurant(id={self.id}, name='{self.name}', health_rating={self.health_rating})>"

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    def calculate_average_health_rating(self):
        if self.inspections:
            ratings = [
                inspection.health_rating for inspection in self.inspections]
            return sum(ratings) / len(ratings)
        else:
            return None

    def update_health_rating(self, new_rating):
        self.health_rating = new_rating
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

class Inspection(Base):
    __tablename__ = 'inspections'

    id = Column(Integer(), primary_key=True)
    inspector = Column(Integer())
    date = Column(Date())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    
    restaurant = relationship('Restaurant', back_populates='inspections')
    inspection_results = relationship('InspectionResult', backref='inspection')

    def __repr__(self):
        return f"<Inspection(id={self.id}, inspector={self.inspector}, date='{self.date}')>"

    def update_inspector(self, new_inspector):
        self.inspector = new_inspector

    def get_most_recent_inspection(self):
        return session.query(Inspection).filter_by(restaurant=self).order_by(Inspection.date.desc()).first()

class InspectionResult(Base):
    __tablename__ = 'inspection_results'

    id = Column(Integer(), primary_key=True)
    results = Column(String())
    inspection_id = Column(Integer(), ForeignKey('inspections.id'))

    def __repr__(self):
        return f"<InspectionResult(id={self.id}, results='{self.results}', inspection_id={self.inspection_id})>"

    @classmethod
    def create_result(cls, session, results, inspection_id):
        new_result = cls(results=results, inspection_id=inspection_id)
        session.add(new_result)
        session.commit()

    def update_results(self, new_results):
        self.results = new_results
        session.commit()
