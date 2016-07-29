from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
 
Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    current_occupancy = Column(Integer)
    maximum_capacity = Column(Integer)
    def getOccupancy(self):
        return self.current_occupancy
    def setOccupancy(self,residents):
        self.current_occupancy= residents
    def setCapacity(self,max_pups):
        self.maximum_capacity = max_pups
    def getCapacity(self):
        return self.maximum_capacity
    
        

    
class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String(100))
    description = Column(String(250))
    needs = Column(String(500))

association_table = Table('association', Base.metadata,
                          Column('puppy_id', Integer, ForeignKey('puppy.id')),
                          Column('adopter_id', Integer, ForeignKey('adopter.id'))
                          )

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phone = Column(String(10))

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    breed = Column(String(30))
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    #    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship(Profile, uselist = False)
    weight = Column(Numeric(10))
    adopters = relationship(Adopter, secondary = association_table, backref = "puppies")
    def adopt(self,owner):
        self.adopters.append( owner )
    def addToShelter(self,shelter_id):
        self.shelter_id = shelter_id
        while self.adopters != []:   #remove previous adopters if any
            self.adopters.pop()




engine = create_engine('sqlite:///puppyshelterfinalproject.db')
 

Base.metadata.create_all(engine)


