from datetime import datetime
from models import Base, engine, session, Restaurant, Inspection, InspectionResult
from sqlalchemy.exc import OperationalError
from faker import Faker

fake = Faker()

def ensure_database_exists():
    try:
        # Try to query the restaurant table
        session.query(Restaurant).first()
    except OperationalError:
        # If we get an OperationalError, the table probably doesn't exist
        print("Creating database tables...")
        Base.metadata.create_all(engine)
        print("Tables created!")

def seed_database():
    # Number of restaurants to seed
    num_restaurants = 100
    
    for _ in range(num_restaurants):
        restaurant_name = fake.company()
        health_rating = fake.random_element(elements=("A", "B", "C", "D", "F"))
        restaurant = Restaurant(name=restaurant_name, health_rating=health_rating)
        session.add(restaurant)

        # Create inspections for those restaurants
        inspection_date = fake.date_this_year(before_today=True, after_today=False)
        inspector_name = fake.first_name()
        inspection = Inspection(inspector=inspector_name, date=datetime.strptime(inspection_date, "%Y-%m-%d").date(), restaurant=restaurant)
        session.add(inspection)

        # Create inspection results for those inspections
        result_text = fake.random_element(elements=("Clean", "Not Clean", "Needs Improvement", "Excellent"))
        result = InspectionResult(results=result_text, inspection=inspection)
        session.add(result)
    
    session.commit()

if __name__ == "__main__":
    ensure_database_exists()
    seed_database()
