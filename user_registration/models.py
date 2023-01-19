from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import database

Base = database.Base


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(Integer)
    password = Column(String)

    profile= relationship('Profile', back_populates='user')

# profile with user id as foreignkey
class Profile(Base):
    __tablename__ = 'Profile'
    id = Column(Integer, primary_key=True, index=True)
    profile_picture: Column(String)
    owner_id = Column(Integer, ForeignKey('Users.id'))

    user = relationship('Users', back_populates='profile')
