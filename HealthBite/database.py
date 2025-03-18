from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URl_DATABASE = 'mysql+pymysql://root:dc2zzsT*a@localhost:3306/healthbite'

engine = create_engine(URl_DATABASE)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()