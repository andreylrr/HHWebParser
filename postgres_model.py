from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Numeric, DateTime, Table, ForeignKey
from datetime import datetime

Base = declarative_base()

skills_association_table = Table('hhstats_vacancies_skills', Base.metadata,
                                 Column("vacancies_id", Integer, ForeignKey('hhstats_vacancies.id')),
                                 Column("skills_id", Integer, ForeignKey('hhstats_skills.id')))

prof_area_association_table = Table('hhstats_vacancies_prof_area', Base.metadata,
                                     Column("vacancies_id", Integer, ForeignKey('hhstats_vacancies.id')),
                                     Column("prof_area_id", Integer, ForeignKey('hhstats_prof_area.id')))

prof_spec_association_table = Table('hhstats_vacancies_prof_spec', Base.metadata,
                                    Column("vacancies_id", Integer, ForeignKey('hhstats_vacancies.id')),
                                    Column("prof_specs_id", Integer, ForeignKey('hhstats_prof_specs.id')))


class Vacancies(Base):
    __tablename__ = 'hhstats_vacancies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    file_name = Column(String)
    min_salary = Column(Integer)
    max_salary = Column(Integer)
    currency = Column(String)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())
    experience = Column(Integer)
    region_id = Column(Integer, ForeignKey("hhstats_regions.id"))
    region = relationship("Regions", primaryjoin="Vacancies.region_id == Regions.id")
    skills = relationship("Skills", secondary=skills_association_table)
    prof_areas = relationship("ProfArea", secondary=prof_area_association_table)
    prof_specs = relationship("ProfSpecs", secondary=prof_spec_association_table)

    def __init__(self, id, name, url, file_name, min_salary, max_salary, currency, experience):
        self.id = id
        self.name = name
        self.url = url
        self.file_name = file_name
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.currency = currency
        self.experience = experience

class Regions(Base):
    __tablename__ = "hhstats_regions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    country = Column(String)
    region = Column(String)
    vac_city = Column(String)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def __init__(self, city, country, region, vac_city, created):
        self.city = city
        self.country = country
        self.region = region
        self.vac_city = vac_city
        self.created = created


class Skills(Base):
    __tablename__ = "hhstats_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def __init__(self, name, created):
        self.name = name
        self.created = created


class ProfSpecs(Base):
    __tablename__ = "hhstats_prof_specs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created = Column(DateTime, default=datetime.now())

    def __init__(self, id, name, created):
        self.id = id
        self.name = name
        self.created = created


class ProfArea(Base):
    __tablename__ = "hhstats_prof_area"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created = Column(DateTime, default=datetime.now())

    def __init__(self, id, name, created):
        self.id = id
        self.name = name
        self.created = created

