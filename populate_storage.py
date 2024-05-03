#!/usr/bin/env python3

"""This script generates dummy data for testing purposes."""

from time import sleep
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from faker import Faker
from random import choice
import sys
from models.place import place_amenity

all_amenities = [
    "Swimming pool",
    "Gym",
    "Spa",
    "Tennis court",
    "Basketball court",
    "Playground",
    "Clubhouse",
    "Fitness center",
    "Yoga studio",
    "Sauna",
    "Hot tub",
    "Barbecue area",
    "Picnic area",
    "Dog park",
    "Walking trails",
    "Bike storage",
    "Movie theater",
    "Game room",
    "Business center",
    "Conference room",
    "Library",
    "Coffee bar",
    "On-site maintenance",
    "24-hour security",
    "Concierge service",
    "Package receiving",
    "Laundry facilities",
    "Dry cleaning service",
    "Car wash area",
    "EV charging stations",
    "On-site parking",
    "Garage parking",
    "Covered parking",
    "Valet parking",
    "Bike rentals",
    "Car rentals",
    "Guest suites",
    "Catering kitchen",
    "Roof deck",
    "Courtyard",
    "Balcony/patio",
    "Fire pit",
    "Garden",
    "Greenhouse",
    "Solarium",
    "Juice bar",
    "Dog grooming station",
    "Pet spa",
    "Dog walking services",
    "Dog obedience training",
    "Indoor pet relief area",
    "Outdoor pet relief area",
    "Pet playground",
    "Pet washing station",
    "Pet-friendly rentals",
    "Wheelchair accessibility",
    "Elevator",
    "Ramp access",
    "Handicap parking",
    "Audio/visual equipment rental",
    "Event planning services",
    "Catering services",
    "Cooking classes",
    "Wine tasting room",
    "Craft room",
    "Art studio",
    "Pottery studio",
    "Music room",
    "Recording studio",
    "Performance space",
    "Dance studio",
    "BBQ/picnic area",
    "Fenced-in yard",
    "Gated entrance",
    "Playground/park",
    "Soccer field",
    "Volleyball court",
    "Cricket pitch",
    "Frisbee golf",
    "Skate park",
    "Community garden",
    "Farmers market",
    "Rooftop lounge",
    "Co-working space",
    "Zen garden",
    "Hammock garden",
    "Ping pong tables",
    "Foosball tables",
    "Pool tables",
    "Shuffleboard",
    "Cornhole",
    "Karaoke room",
    "Bocce ball court",
    "Putting green",
    "Golf simulator",
    "Virtual reality room",
    "Bowling alley",
    "Rock climbing wall",
    "Mini golf course",
    "Arcade room"
]


def create_dummy_data(number_of_instances):
    """
    Creates dummy data for testing purposes.

    Args:
        number_of_instances (int): The number of instances to create.
    """
    fake = Faker()
    city_ids = []
    user_ids = []
    place_ids = []
    amenity_ids = []

    for _ in range(number_of_instances):
        state_obj = State(name=fake.state())
        print("Created state: {} - {}".format(state_obj.name, state_obj.id))
        state_obj.save()
        sleep(0.1)

        print("\t Creating cities for the state: {}".format(state_obj.name))
        for _ in range(number_of_instances * 2):
            city_obj = City(state_id=state_obj.id, name=fake.city())
            print("\t\t Created city: {} - {}".format(
                city_obj.name, city_obj.id)
            )
            city_ids.append(city_obj.id)
            city_obj.save()
            sleep(0.1)

    print("\nCreating users")
    for _ in range(number_of_instances):
        # create users
        user_obj = User(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password()
        )
        print("\t Created user: {} - {}".format(user_obj.id, user_obj.email))
        user_ids.append(user_obj.id)
        user_obj.save()
        sleep(0.1)

    # create some places objects
    print("\nCreating Places")
    for c_id in city_ids:
        for _ in range(number_of_instances * 2):
            user_id = choice(user_ids)
            city_id = c_id
            city = storage.get(City, city_id)
            print("\t Adding places for city: {}".format(city.name))
            place_obj_1 = Place(
                user_id=user_id,
                city_id=city_id,
                name=fake.city(),
                longitude=float(fake.longitude()),
                latitude=float(fake.latitude()),
                description=fake.sentence(),
                number_of_rooms=fake.random_digit(),
                number_of_bathrooms=fake.random_digit(),
                price_by_night=fake.random_int()
            )
            place_obj_2 = Place(
                user_id=user_id,
                city_id=city_id,
                name=fake.city(),
                longitude=float(fake.longitude()),
                latitude=float(fake.latitude()),
                description=fake.sentence(),
                number_rooms=fake.random_digit(),
                number_bathrooms=fake.random_digit(),
                price_by_night=fake.random_int()
            )

            place_obj_1.save()
            sleep(0.1)
            place_obj_2.save()
            place_ids.append(place_obj_1.id)
            place_ids.append(place_obj_2.id)
            print("\t\t Added place: {} - {}".
                  format(place_obj_1.id, place_obj_1.name))
            print("\t\t Added place: {} - {}".
                  format(place_obj_2.id, place_obj_2.name))
            sleep(0.1)

    # let's have some reviews for each of these places
    print("\nAdding reviews")
    for obj in place_ids:
        place_obj = storage.get(Place, obj)
        review_obj = Review(
            user_id=user_id, place_id=place_obj.id, text=fake.sentence()
        )
        review_obj.save()
        print("\t Added review: {} - {}".
              format(place_obj.name, review_obj.text)
              )
        sleep(0.1)

    # create some amenities
    print("\nCreating amenities")
    for _ in place_ids:
        for _ in range(number_of_instances):
            amenity_obj = Amenity(name=choice(all_amenities))
            amenity_ids.append(amenity_obj.id)
            amenity_obj.save()
            sleep(0.1)

            print("\t Added amenity: {} - {}".
                  format(amenity_obj.name, amenity_obj.id))

    # add amenities to places
    print("\nAdding amenities to places")
    for obj in place_ids:
        place_obj = storage.get(Place, obj)
        for _ in range(number_of_instances):
            amenity_obj = storage.get(Amenity, choice(amenity_ids))
            place_obj.amenities.append(amenity_obj)
            place_obj.save()
            print("\t Added amenity: {} to place: {}".
                  format(amenity_obj.name, place_obj.name))
            sleep(0.1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <number_of_instance>".format(sys.argv[0]))
        sys.exit(1)

    create_dummy_data(int(sys.argv[1]))
