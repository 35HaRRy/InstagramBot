import os

from pymongo import MongoClient


class QuoteService:
    def __init__(self):
        self.mongo_client = MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
        self.db = self.mongo_client["instagram_bot_db"]
        self.quotes_collection = self.db["quotes"]

    def get_unshared_quote(self):
        """MongoDB'den paylaşılmamış bir alıntı al"""
        quote = self.quotes_collection.find_one({"isShared": False})

        return quote
        
    def mark_quote_as_shared(self, quote_id):
        # Alıntıyı paylaşıldı olarak işaretle
        self.quotes_collection.update_one(
            {"_id": quote_id},
            {"$set": {"isShared": True}}
        )
