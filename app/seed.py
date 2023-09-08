from sqlalchemy.exc import SAWarning
import warnings
from datetime import date
from models import engine, session, Restaurant, Inspection, InspectionResult
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=SAWarning)

fake = Faker()

set_dates = [date(2023, 9, i) for i in range(1, 21)]

if __name__ == "__main__":

    engine = create_engine('sqlite:///diner_tracker.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Inspection).delete()
    session.query(InspectionResult).delete()
    session.commit()

    print("seeding.....")

    for i in range(20):
        restaurant_name = fake.company()
        health_rating = fake.random_element(
            elements=("A", "B", "C", "D", "F"))
        restaurant = Restaurant(
            name=restaurant_name, health_rating=health_rating)
        session.add(restaurant)

        # Create inspections for those restaurants
        inspection_date = set_dates[i]
        inspector_name = fake.first_name()
        inspection = Inspection(inspector=inspector_name, assigned_date=inspection_date, restaurant=restaurant)
        session.add(inspection)

        # Create inspection results for those inspections
        result_text = fake.random_element(
            elements=("Clean", "Not Clean", "Needs Improvement", "Excellent"))
        
        # Here's the change: Instead of inspection, we use inspection_name
        result = InspectionResult(results=result_text, inspection_name=inspection)
        session.add(result)

    session.commit()
