from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
config_filename = 'postgresql_config.ini'
config_path = os.path.join(current_dir, config_filename)


config = configparser.ConfigParser()
config.read(config_path)


db_config = config['postgresql']
DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
