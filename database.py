#!/usr/bin/env python3
"""
MongoDB Database Configuration and Helper Functions
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoDB:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.database_url, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client.rewear_db
            print("✅ Connected to MongoDB successfully!")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        if self.db is None:
            if not self.connect():
                return None
        return self.db[collection_name]
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("🔒 MongoDB connection closed")

# Global MongoDB instance
mongo_db = MongoDB()

# Collection helper functions
def get_users_collection():
    return mongo_db.get_collection('users')

def get_items_collection():
    return mongo_db.get_collection('items')

def get_exchanges_collection():
    return mongo_db.get_collection('exchanges')

def get_activity_logs_collection():
    return mongo_db.get_collection('activity_logs')

def get_wishlist_collection():
    return mongo_db.get_collection('wishlist')

# CRUD Operations
def insert_document(collection_name, document):
    """Insert a document into a collection"""
    collection = mongo_db.get_collection(collection_name)
    if collection is not None:
        result = collection.insert_one(document)
        return result.inserted_id
    return None

def find_documents(collection_name, query=None, limit=None):
    """Find documents in a collection"""
    collection = mongo_db.get_collection(collection_name)
    if collection is not None:
        if query is None:
            query = {}
        cursor = collection.find(query)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    return []

def find_one_document(collection_name, query):
    """Find one document in a collection"""
    collection = mongo_db.get_collection(collection_name)
    if collection is not None:
        return collection.find_one(query)
    return None

def update_document(collection_name, query, update_data):
    """Update a document in a collection"""
    collection = mongo_db.get_collection(collection_name)
    if collection is not None:
        result = collection.update_one(query, {'$set': update_data})
        return result.modified_count > 0
    return False

def delete_document(collection_name, query):
    """Delete a document from a collection"""
    collection = mongo_db.get_collection(collection_name)
    if collection is not None:
        result = collection.delete_one(query)
        return result.deleted_count > 0
    return False

def count_documents(collection_name, query=None):
    """Count documents in a collection"""
    collection = mongo_db.get_collection(collection_name)
    if collection is not None:
        if query is None:
            query = {}
        return collection.count_documents(query)
    return 0

# User-specific helper functions
def get_user_by_email(email):
    """Get user by email"""
    return find_one_document('users', {'email': email})

def get_user_by_id(user_id):
    """Get user by ID"""
    return find_one_document('users', {'id': user_id})

def get_user_items(user_id):
    """Get all items for a user"""
    return find_documents('items', {'user_id': user_id})

def get_user_exchanges(user_id):
    """Get all exchanges for a user"""
    return find_documents('exchanges', {'$or': [{'requester_id': user_id}, {'owner_id': user_id}]})

def get_user_activities(user_id, limit=50):
    """Get recent activities for a user"""
    return find_documents('activity_logs', {'user_id': user_id}, limit)

def get_user_wishlist(user_id):
    """Get user's wishlist"""
    return find_documents('wishlist', {'user_id': user_id})

# Test connection function
def test_connection():
    """Test MongoDB connection"""
    try:
        if mongo_db.client:
            # Test ping
            mongo_db.client.admin.command('ping')
            
            # Test database access
            collections = mongo_db.db.list_collection_names()
            
            print("✅ MongoDB Connection Test Successful!")
            print(f"📊 Database: {mongo_db.db.name}")
            print(f"📁 Collections: {collections}")
            
            # Show collection counts
            for collection_name in ['users', 'items', 'exchanges', 'activity_logs', 'wishlist']:
                count = count_documents(collection_name)
                print(f"   - {collection_name}: {count} documents")
            
            return True
    except Exception as e:
        print(f"❌ MongoDB Connection Test Failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
