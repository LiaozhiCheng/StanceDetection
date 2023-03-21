from pymongo import MongoClient

DB = MongoClient('mongodb://localhost:27017')['Media_data']


FB_COLLECTION = DB['fb_raw']