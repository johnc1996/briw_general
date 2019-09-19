from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Unicode, Sequence, TIMESTAMP, Boolean, Column, Integer, ForeignKey
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm.session import object_session

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, Sequence('%s_id_seq'%__tablename__), primary_key=True)
    first_name = Column(Unicode(64))
    last_name = Column(Unicode(64))
    default_configured_drink_id = Column(Integer, default=None)
    email = Column(Unicode(128), unique=True, nullable=False )

    def __init__(self, first_name, last_name, email,
                  default_configured_drink_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if default_configured_drink_id is not None:
            self.default_configured_drink_id = default_configured_drink_id

    def get_id(self):
        return self.id

    def get_default_configured_drink(self):
        drink_id = self.default_configured_drink_id
        session = object_session(self) 
        return session.query(Drink).filter(Drink.id == self.default_configured_drink_id).first()
    
    def get_default_configured_drink_name(self):
        return get_default_configured_drink().name

    def set_default_configured_drink(self, drink_name):
        session = object_session(self) 
        target_drink = session.query(Drink).filter(Drink.name == self.name).first()
        if target_drink is None:
            target_drink = new_drink(session, drink_name)
            self.default_configured_drink_id = target_drink.id

class Person_Group_Association(Base):
        __tablename__ = 'person_group_association'
        group_id = Column(Integer)
        person_id = Column(Integer, primary_key=True)

class Drink(Base):
    __tablename__ = 'drink'

    id = Column(Integer, Sequence('%s_id_seq'%__tablename__), primary_key=True)
    name = Column(Unicode(32))

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Person_Group(Base):
    __tablename__ = 'person_group'
    id = Column(Integer, Sequence('%s_id_seq'%__tablename__), primary_key=True)
    name = Column(Unicode(64))
    is_temp = Column(Boolean, default=False)
    round_id = Column(Integer, default=None)
    group_epoch = Column(TIMESTAMP)

    def __init__(self, name):
        self.name = name
        self.group_epoch = datetime.now()

class Configured_Drink(Base):
    __tablename__ = 'configured_drink'
    id = Column(Integer, Sequence('%s_id_seq'%__tablename__), primary_key=True)
    name = Column(Unicode(64))
    drink_id = Column(Integer)
    serving_note = Column(Unicode(128))

    def __init__(self, name, drink_id, serving_note=''):
        self.name = name
        self.drink_id = drink_id
        self.serving_note = serving_note

class Round(Base):
    __tablename__ = 'round'
    id = Column(Integer, Sequence('%s_id_seq'%__tablename__), primary_key=True)
    request_epoch = Column(TIMESTAMP)
    acccept_epoch = Column(TIMESTAMP)
    complete_epoch = Column(TIMESTAMP)
    status = Column(Unicode(24))
    maker_person_id = Column(Integer)
    base_group_association_id = Column(Integer)

# initialisation helpers

def new_person(session, first_name, last_name, email, default_configured_drink_id=None):
    a_person = Person(first_name, last_name, email, default_configured_drink_id)
    session.add(a_person)
    session.commit()
    return a_person

def new_drink(session, name):
    a_drink = Drink(name)
    session.add(a_drink)
    session.commit()
    return a_drink

def get_drink_by_id(session, id):
    return session.query(Drink).filter(Drink.id == id).first()

def get_person_by_email(session, email):
    return session.query(Person).filter(Person.email == email).first()

def make_session():
    engine = create_engine('postgresql://postgres:docker@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    return Session()












# engine = create_engine('postgresql://postgres:docker@localhost:5432/postgres')

# Session = sessionmaker(bind=engine)
# Base.metadata.create_all(engine)
# session = Session()

# p = Person('Harry2')
# session.add(p)

# session.commit()


#p = session.query(Person).first()

# if __name__ == "__main__":

#     # Run this file directly to create the database tables.
#     print "Creating database tables..."
#     db.create_all()
#     print "Done!"