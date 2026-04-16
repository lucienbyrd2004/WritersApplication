import os
import mysql.connector as mysqlconnector
from mysql.connector import errorcode
import sqlalchemy 
from dotenv import load_dotenv

#Login for the database
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")


def getconn():
    conn= mysqlconnector.connect(
        user = DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        host=DB_HOST
        )
    return conn

pool = sqlalchemy.create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}",
    )

def connecttodatabase():
    try:
        conn= mysqlconnector.connect(
            user = DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            host=DB_HOST
        )
    except mysqlconnector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()
        print("Successful connection")

connecttodatabase()