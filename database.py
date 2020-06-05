from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser as cfg


config = cfg.ConfigParser()
config.read("../web_app/hh_config.ini")
engine = create_engine(config["PostgreSQL"]["path"])
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = Session()
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def create_db():
    Base.metadata.drop_all(engine)
    # Создание новых таблиц
    Base.metadata.create_all(engine)
    db_session.close()
