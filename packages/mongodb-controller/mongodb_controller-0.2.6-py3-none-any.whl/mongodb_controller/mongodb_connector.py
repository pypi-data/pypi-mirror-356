from pymongo import MongoClient
from .mongodb_consts import MONGODB_URI

client = MongoClient(MONGODB_URI)

db_test = client['database-test']
collection_test = db_test['collection-hello']