#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Bakery, BakedGood

fake = Faker()

with app.app_context():

    # Delete all existing bakeries and baked goods
    BakedGood.query.delete()
    Bakery.query.delete()

    # Create a list of bakeries
    bakeries = []
    for i in range(20):
        b = Bakery(
            name=fake.company()
        )
        bakeries.append(b)

    # Add the bakeries to the database
    db.session.add_all(bakeries)

    # Try to commit the changes to the database
    try:
        db.session.commit()
    except Exception as e:
        # Handle the error
        print(e)

    # Create a list of baked goods
    baked_goods = []
    names = []
    for i in range(200):

        name = fake.first_name()
        while name in names:
            name = fake.first_name()
        names.append(name)

        bg = BakedGood(
            name=name,
            price=randint(1, 10),
            bakery_id=rc(bakeries).id
        )

        baked_goods.append(bg)

    # Add the baked goods to the database
    db.session.add_all(baked_goods)

    # Try to commit the changes to the database
    try:
        db.session.commit()
    except Exception as e:
        # Handle the error
        print(e)

    # Make the most expensive baked good even more expensive
    most_expensive_baked_good = rc(baked_goods)
    most_expensive_baked_good.price = 100

    # Update the database
    db.session.add(most_expensive_baked_good)
    db.session.commit()


