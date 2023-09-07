from sqlalchemy import create_engine
from models import Restaurant, Inspection , InspectionResult
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import date

engine = create_engine('sqlite:///diner_tracker.db')
Session = sessionmaker(bind=engine)
session=Session()


fake=Faker()
# generated dates based on  the no of inspectors
set_dates = [date(2023, 9, i) for i in range(1, 16)]

if __name__ == '__main__':
    session.query(Restaurant).delete()
    session.query(Inspection).delete()
    restaurant = []

    for i in range(15):
        new_restaurant = Restaurant(name=fake.company())
        session.add(new_restaurant)
        session.commit()
        restaurant.append(new_restaurant)
        print('Done')

    for i in range(15):
        inspector = fake.name()
        # assign each date for an inspector
        assigned_date = set_dates[i]

        # new_inspector = Inspection(name_inspector=inspector_name, assigned_date=assigned_date)
        new_inspector = Inspection(inspector=inspector, assigned_date=assigned_date)
        session.add(new_inspector)
        print('finished')

    session.commit()

        