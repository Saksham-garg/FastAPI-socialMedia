from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi',
#                             user='postgres', password='root4321', cursor_factory=RealDictCursor)

#     cursor = conn.cursor()
#     print("Database connection was successfull.")
# except Exception as error:
#     print(error)


 