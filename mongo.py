from pymongo import MongoClient
from dotenv import load_dotenv
import os
import numpy
load_dotenv()
MONGOPASSWORD = os.getenv('MONGO')
DATABASE = os.getenv('DB')
class Mongo:
    def __init__(self):
        self.client = self.get_collection_cursor()


    def get_collection_cursor(self):
        client = MongoClient(f'mongodb+srv://alimongodb:{MONGOPASSWORD}@cluster0.r1xcz.mongodb.net/<dbname>?retryWrites=true&w=majority')
        db = client.DATABASE
        cursor = db.birminghamratings
        return cursor

    def show_greater_than_mean_ratings(self, cursor, rating):
        gt = cursor.find({'MeanRating': {'$gt': rating}})
        for i in gt:
            print(f'Postcode: {i["Postcode"]}\nMean Rating: {i["MeanRating"]}\n ---------------')

    def show_lesser_than_mean_ratings(self, cursor, rating):
        lt = cursor.find({'MeanRating': {'$lt': rating}})
        for i in lt:
            print(f'Postcode: {i["Postcode"]}\nMean Rating: {i["MeanRating"]}\n ---------------')

    # def make_mean_ratings_graph(self, cursor):

    def prepare_mongo_insert(self, data):
        data1 = []
        counter = 1
        for i in data:
            x = {
                '_id': counter,
                'Postcode': i['Postcode'],
                'MeanRating': numpy.mean(i['Ratings'])
            }
            data1.append(x)
            counter += 1
        return data1
    def insert_into_collection(self, query, collection):
        try:
            collection.insert_many(query)
        except Exception as e:
            return e 


