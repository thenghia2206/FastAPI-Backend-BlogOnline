from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2


SQLALCHEMY_DATABASE_URL = "postgresql://xzcosycukzzrff:cc1a8d2008eac70318ed5e40494625b9202177852500dec83059a7ebbefadde3@ec2-54-159-175-38.compute-1.amazonaws.com:5432/dcidjhp5s2smfd"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         cnx = mysql.connector.connect(
#             user='root', password='22062001', host='127.0.0.1', database='test')
#         print("Database connection was succesfull!")
#         cursor = cnx.cursor(dictionary=True)
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
