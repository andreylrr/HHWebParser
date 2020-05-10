from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    created = Column(DateTime(), default=datetime.now)
    password = Column(String(50))

    def __init__(self, name=None, last_name=None, email=None, created=None, password=None):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.created = created
        self.password = password

    def __repr__(self):
        return f'<User {self.name} {self.email}>'


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    region = Column(String(150))
    text_request = Column(String(150))
    file_name = Column(String(250))
    status = Column(Integer)
    created = Column(DateTime(), default=datetime.now)
    updated = Column(DateTime(), default=None)
    vacancy_number = Column(Integer)
    user = relationship("User", backref="requests")

    def __init__(self, user_id=None, region=None, text_request=None, file_name=None, status=None,
                 created=None, updated=None, vacancy_number=None):
        self.user_id = user_id
        self.region = region
        self.text_request = text_request
        self.file_name = file_name
        self.status = status
        self.created = created
        self.updated = updated
        self.vacancy_number = vacancy_number

    def __repr__(self):
        return f'Request {self.region} {self.text_request}'


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text(500))
    email = Column(String(100))
    name = Column(String(100))

    def __init__(self, id=None, name=None, text=None, email=None):
        self.id = id
        self.text = text
        self.email = email
        self.name = name

    def __repr__(self):
        return f'Request {self.id} {self.email} {self.name}'
