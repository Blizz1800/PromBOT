from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB = MongoClient(getenv("MONGO_URI"))['vendermejor']
