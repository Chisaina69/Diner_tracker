# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
import warnings
from sqlalchemy import exc as sa_exc

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=sa_exc.SAWarning)

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
    # finds restaurant by their name
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    # shows health ratings for each inspection after checking restaurants
    def calculate_average_health_rating(self):
        if self.inspections:
            ratings = [
                inspection.health_rating for inspection in self.inspections]
            # calculates the average by adding all ratings then dividing by the total number(len) of inspection in ratings
            return sum(ratings) / len(ratings)
        else:
            return None
    # updates the health rating then commits

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
    assigned_date = Column(Date())
    # Define relationship
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    # One to many relationship
    restaurant = relationship('Restaurant', back_populates='inspections')

    inspection_results = relationship('InspectionResult', back_populates='inspection_name')

    def __repr__(self):
        return f"<Inspection(id={self.id}, inspector={self.inspector}, date='{self.assigned_date}')>"
    # Basically assisnges an inspector and update

    def update_inspector(self, new_inspector):
        self.inspector = new_inspector
        # session.commit() inoder to commit changes to the database

    def get_most_recent_inspection(self):
        return session.query(Inspection).filter_by(restaurant=self).order_by(Inspection.date.desc()).first()


class InspectionResult(Base):
    __tablename__ = 'inspection_results'

    id = Column(Integer(), primary_key=True)
    results = Column(String())
    inspection_id = Column(Integer(), ForeignKey('inspections.id'))

    inspection_name = relationship(
        'Inspection', back_populates='inspection_results')

    def __repr__(self):
        return f"<InspectionResult(id={self.id}, results='{self.results}', inspection_id={self.inspection_id})>"

    @classmethod
    def create_result(cls, session, results, inspection_id):
        new_result = cls(results=results, inspection_id=inspection_id)
        session.add(new_result)
        session.commit()
        return session.query(cls).filter_by(inspection_id=inspection_id).all()

    def update_results(self, new_results):
        self.results = new_results
        session.commit()


# inspection1 = session.query(Inspection).first()
# print(inspection1.restaurant)
# inspection1 = session.query(Inspection).first()
# if inspection1:
#     print(inspection1.restaurant)
# else:
#     print("No inspection found.")
