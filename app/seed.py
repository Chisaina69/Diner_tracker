from models import Base, engine, session, Restaurant, Inspection, InspectionResult
from sqlalchemy.exc import OperationalError

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
    # Create some sample restaurants
    restaurant1 = Restaurant(name="Burger King", health_rating="A")
    restaurant2 = Restaurant(name="Taco Bell", health_rating="B")
    session.add(restaurant1)
    session.add(restaurant2)
    
    # Create inspections for those restaurants
    inspection1 = Inspection(inspector="John", date="2023-09-06", restaurant=restaurant1)
    inspection2 = Inspection(inspector="Jane", date="2023-09-05", restaurant=restaurant2)
    session.add(inspection1)
    session.add(inspection2)
    
    # Create inspection results for those inspections
    result1 = InspectionResult(results="Clean", inspection=inspection1)
    result2 = InspectionResult(results="Not Clean", inspection=inspection2)
    session.add(result1)
    session.add(result2)
    
    session.commit()

if __name__ == "__main__":
    ensure_database_exists()
    seed_database()
