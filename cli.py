import argparse
import sys
import os

# Ensure that the directory containing the 'app' folder is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import session, Restaurant, Inspection, InspectionResult

# CRUD Functions

def add_restaurant(name, health_rating):
    restaurant = Restaurant(name=name, health_rating=health_rating)
    session.add(restaurant)
    session.commit()
    print(f"Restaurant {name} added successfully!")

def list_restaurants():
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        print(f"ID: {restaurant.id}, Name: {restaurant.name}, Health Rating: {restaurant.health_rating}")

def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant:
        session.delete(restaurant)
        session.commit()
        print(f"Restaurant with ID {restaurant_id} deleted successfully!")
    else:
        print(f"Restaurant with ID {restaurant_id} not found!")

# CLI setup using argparse

parser = argparse.ArgumentParser(description="Diner Tracker CLI")
subparsers = parser.add_subparsers(dest="command")

# Adding a subcommand for adding a restaurant
add_parser = subparsers.add_parser('add-restaurant')
add_parser.add_argument('name', help="Name of the restaurant")
add_parser.add_argument('health_rating', help="Health rating of the restaurant")

# Adding a subcommand for listing all restaurants
list_parser = subparsers.add_parser('list-restaurants')

# Adding a subcommand for deleting a restaurant
delete_parser = subparsers.add_parser('delete-restaurant')
delete_parser.add_argument('restaurant_id', type=int, help="ID of the restaurant to be deleted")

# Linking Arguments to Functions

args = parser.parse_args()

if args.command == "add-restaurant":
    add_restaurant(args.name, args.health_rating)
elif args.command == "list-restaurants":
    list_restaurants()
elif args.command == "delete-restaurant":
    delete_restaurant(args.restaurant_id)
else:
    print("Invalid command. Use -h or --help for guidance.")
