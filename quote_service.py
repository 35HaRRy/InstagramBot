import os

from pymongo import MongoClient


class QuoteService:
    def __init__(self):
        self.mongo_client = MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
        self.db = self.mongo_client["quotes_db"]
        self.quotes_collection = self.db["quotes"]

        self.last_used_quote = None

    def get_unshared_quote(self):
        """MongoDB'den paylaşılmamış bir alıntı al"""
        quote = self.quotes_collection.find_one({"IsShared": False})

        if quote:
            # Alıntıyı paylaşıldı olarak işaretle
            self.quotes_collection.update_one(
                {"_id": quote["_id"]},
                {"$set": {"IsShared": True}}
            )
            self.last_used_quote = quote["text"]

            return quote["text"]

        return None
