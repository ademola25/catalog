#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, SpaItem, User

engine = create_engine('sqlite:///spa_category.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Tijani Ademola", email="tijaniademola25@gmail.com",
             picture='https://www.ienglishstatus.com/wp-content/uploads/2018/04/Anonymous-Whatsapp-profile-picture.jpg')
session.add(User1)
session.commit()


# Category of  Reception Desk
category1 = Category(user_id=1, name="Reception Desk")
session.add(category1)
session.commit()

# Category of Men Salon
category2 = Category(user_id=1, name="Men Salon")
session.add(category2)
session.commit()

# Category of Beauty Salon
category3 = Category(user_id=1, name="Beauty Salon")
session.add(category3)
session.commit()

# Category of Facial
category4 = Category(user_id=1, name="Facial")
session.add(category4)
session.commit()

# Category of Pedicure / Manicure
category5 = Category(user_id=1, name="Pedicure / Manicure")
session.add(category5)
session.commit()

# Category of  Massaging
category6 = Category(user_id=1, name="Massage")
session.add(category6)
session.commit()

# Category of Lounge
category7 = Category(user_id=1, name="Lounge")
session.add(category7)
session.commit()

# Category of Fitness Equipment Studio
category8 = Category(user_id=1, name="Fitness Equipment Studio")
session.add(category8)
session.commit()

# Category of Sales of Salon Materials
category9 = Category(user_id=1, name="Sales of Salon Materials")
session.add(category9)
session.commit()

# Category of  Laundry Room
category10 = Category(user_id=1, name="Laundry Room")
session.add(category10)
session.commit()

# Adding  Items into category1
spaItem1 = SpaItem(user_id=1, name="Customer Care Representative",
                             description="This desk see to every the \
                              satisfaction of every customer that walks into \
                               the Spa, Enquiries is made through the desk and also  \
                              every customer make payment to the Desk Rep.",
                             categories=category1)
session.add(spaItem1)
session.commit()

# Adding  Items into category2
spaItem1 = SpaItem(user_id=1, name="Barbers",
                             description="These are the stylist that see to \
                              the haircut of every male customer, they are in \
                               charge the Haircut, Hair-dye, washing, \
                              Dred-lock and Hair-tint.",
                             categories=category2)
session.add(spaItem1)
session.commit()

# Adding  Items into category3
spaItem1 = SpaItem(user_id=1, name="Female stylist",
                             description="These are the stylist that see to \
                              the hair-beauty of every female customer, they are in charge \
                               the braids, Weaving, washing, and dred locks and \
                              Also Hair-tint for our female customer.",
                             categories=category3)
session.add(spaItem1)
session.commit()

# Adding  Items into category4
spaItem1 = SpaItem(user_id=1, name="Beauty therapist",
                             description="Here is where they carry out treatments \
                              to improve a person's appearance, such as facials, \
                               removal of unwanted hair, etc.",
                             categories=category4)
session.add(spaItem1)
session.commit()

# Adding  Items into category5
spaItem1 = SpaItem(user_id=1, name="Nail Tech",
                             description="Here is where work is done on the hands \
                              and feet, providing treatments to groom, \
                              fingernails and toenails.",
                             categories=category5)
session.add(spaItem1)
session.commit()

# Adding  Items into category6
spaItem1 = SpaItem(user_id=1, name="Masseur",
                             description="Here we provide proffessional \
                              masseur that give massage professionally. \
                               we have both male and female so customer \
                               have the right to choose whoever they want.",
                             categories=category6)
session.add(spaItem1)
session.commit()

# Adding  Items into category7
spaItem1 = SpaItem(user_id=1, name="Lounge Bar",
                             description="a place for sitting, waiting, etc, \
                             While our customer are waiting for there turn, \
                            they deserve some Royal treatment, so \
                            we serve them coffee or any drink of there choice.",
                             categories=category7)
session.add(spaItem1)
session.commit()

# Adding  Items into category8
spaItem1 = SpaItem(user_id=1, name="Trainer",
                             description="A standby trainer at a Fitness Studio which \
                              spans over two levels and is equipped with the worlds \
                               leading fitness equipment, brands including Alphafit, \
                               Rogue, Iron Edge, Life, Fitness and Hammer Strength. \
                               Our cardio stations are entertainment enabled with \
                                digital TV, radio, and USB, compatible so you can \
                                watch and listen to what you like.",
                             categories=category8)
session.add(spaItem1)
session.commit()

# Adding  Items into category9
spaItem1 = SpaItem(user_id=1, name="Sales Rep",
                             description="work with customers to find what they want, \
                              create solutions and ensure a smooth sales process.",
                             categories=category9)
session.add(spaItem1)
session.commit()



# Adding  Items into category10
spaItem1 = SpaItem(user_id=1, name="Cleaner",
                             description="Here is where towel used and clothes   \
                              are washed and dried. it is well equipped with  \
                              an automatic washing machine and clothes dryer.",
                             categories=category10)
session.add(spaItem1)
session.commit()




print "added menu items!"
