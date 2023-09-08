import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Replace with your actual module name
from models import Restaurant, Inspection, InspectionResult

# Initialize the database engine and session
engine = create_engine('sqlite:///diner_tracker.db')
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    "Restaurant Tracker"


@click.command()
@click.option('--name', prompt='Enter the restaurant name', help='Name of the restaurant')
@click.option('--health-rating', prompt='Enter the health rating', type=str, help='Health rating of the restaurant')
def add_restaurant(name, health_rating):
    """Add restaurant"""
    new_restaurant = Restaurant(name=name, health_rating=health_rating)
    session.add(new_restaurant)
    session.commit()
    click.echo(f"Added restaurant: {new_restaurant}")


@click.command()
@click.option('--name', prompt='Enter the restaurant name', help='Name of the restaurant')
@click.option('--new-rating', prompt='Enter the new health rating', type=str, help='New health rating for the restaurant')
def update_rating(name, new_rating):
    """Update rating"""
    restaurant = Restaurant.find_by_name(name)
    if restaurant:
        restaurant.update_health_rating(new_rating)
        click.echo(f"Updated rating for {name} to {new_rating}")
    else:
        click.echo("Restaurant not found.")


@click.command()
@click.option('--name', prompt='Enter the restaurant name', help='Name of the restaurant')
def delete_restaurant(name):
    """Delete restaurant"""
    restaurant = Restaurant.find_by_name(name)
    if restaurant:
        restaurant.delete()
        click.echo(f"Deleted restaurant: {name}")
    else:
        click.echo("Restaurant not found.")


@click.command()
def list_restaurants():
    """List restaurants"""
    restaurants = session.query(Restaurant).all()
    if restaurants:
        for restaurant in restaurants:
            click.echo(restaurant)
    else:
        click.echo("No restaurants found.")


@click.command()
@click.option('--restaurant-name', prompt='Enter the restaurant name', help='Name of the restaurant')
@click.option('--inspection-results', prompt='Enter the inspection results', help='Inspection results for the restaurant')
def add_inspection_result(restaurant_name, inspection_results):
    """Add inspection results"""
    restaurant = Restaurant.find_by_name(restaurant_name)
    if restaurant:
        most_recent_inspection = restaurant.get_most_recent_inspection()
        if most_recent_inspection:
            InspectionResult.create_result(
                session, inspection_results, most_recent_inspection.id)
            click.echo(f"Added inspection result for {restaurant_name}")
        else:
            click.echo(f"No inspections found for {restaurant_name}.")
    else:
        click.echo("Restaurant not found.")


cli.add_command(add_restaurant)
cli.add_command(update_rating)
cli.add_command(delete_restaurant)
cli.add_command(list_restaurants)
cli.add_command(add_inspection_result)

if __name__ == '__main__':
    cli()
