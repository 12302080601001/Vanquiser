#!/usr/bin/env python3
"""
Migration script to transfer data from JSON files to MongoDB
"""
import json
import os
from datetime import datetime
from database import (
    mongo_db, insert_document, find_documents, count_documents,
    get_users_collection, get_items_collection, get_exchanges_collection,
    get_activity_logs_collection, get_wishlist_collection
)

def load_json_file(file_path):
    """Load data from JSON file"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return []
    else:
        print(f"⚠️  File not found: {file_path}")
        return []

def migrate_collection(json_file, collection_name, description):
    """Migrate data from JSON file to MongoDB collection"""
    print(f"\n📁 Migrating {description}...")
    
    # Load JSON data
    data = load_json_file(json_file)
    
    if not data:
        print(f"   ⚠️  No data found in {json_file}")
        return 0
    
    # Get collection
    collection = mongo_db.get_collection(collection_name)
    if collection is None:
        print(f"   ❌ Failed to get collection: {collection_name}")
        return 0
    
    # Check if data already exists
    existing_count = count_documents(collection_name)
    if existing_count > 0:
        print(f"   ⚠️  Collection {collection_name} already has {existing_count} documents")
        response = input(f"   🤔 Do you want to clear and re-import? (y/N): ").lower()
        if response == 'y':
            collection.delete_many({})
            print(f"   🗑️  Cleared existing data")
        else:
            print(f"   ⏭️  Skipping {collection_name}")
            return existing_count
    
    # Insert data
    try:
        if data:
            result = collection.insert_many(data)
            inserted_count = len(result.inserted_ids)
            print(f"   ✅ Inserted {inserted_count} documents into {collection_name}")
            return inserted_count
        else:
            print(f"   ⚠️  No data to insert for {collection_name}")
            return 0
    except Exception as e:
        print(f"   ❌ Error inserting data into {collection_name}: {e}")
        return 0

def verify_migration():
    """Verify that all data was migrated correctly"""
    print("\n🔍 Verifying migration...")
    
    collections_info = [
        ('users', 'data/users.json', 'Users'),
        ('items', 'data/items.json', 'Items'),
        ('exchanges', 'data/exchanges.json', 'Exchanges'),
        ('activity_logs', 'data/activity_logs.json', 'Activity Logs'),
        ('wishlist', 'data/wishlist.json', 'Wishlist')
    ]
    
    all_good = True
    
    for collection_name, json_file, description in collections_info:
        json_data = load_json_file(json_file)
        mongo_count = count_documents(collection_name)
        json_count = len(json_data) if json_data else 0
        
        status = "✅" if mongo_count == json_count else "❌"
        print(f"   {status} {description}: JSON={json_count}, MongoDB={mongo_count}")
        
        if mongo_count != json_count:
            all_good = False
    
    if all_good:
        print("\n🎉 Migration verification successful! All data migrated correctly.")
    else:
        print("\n⚠️  Migration verification found discrepancies. Please check the data.")
    
    return all_good

def create_indexes():
    """Create indexes for better performance"""
    print("\n🔧 Creating database indexes...")
    
    try:
        # Users collection indexes
        users_collection = get_users_collection()
        users_collection.create_index("email", unique=True)
        users_collection.create_index("id", unique=True)
        print("   ✅ Created indexes for users collection")
        
        # Items collection indexes
        items_collection = get_items_collection()
        items_collection.create_index("id", unique=True)
        items_collection.create_index("user_id")
        items_collection.create_index("category")
        items_collection.create_index("status")
        print("   ✅ Created indexes for items collection")
        
        # Exchanges collection indexes
        exchanges_collection = get_exchanges_collection()
        exchanges_collection.create_index("id", unique=True)
        exchanges_collection.create_index("requester_id")
        exchanges_collection.create_index("owner_id")
        exchanges_collection.create_index("status")
        print("   ✅ Created indexes for exchanges collection")
        
        # Activity logs collection indexes
        activity_collection = get_activity_logs_collection()
        activity_collection.create_index("id", unique=True)
        activity_collection.create_index("user_id")
        activity_collection.create_index("timestamp")
        print("   ✅ Created indexes for activity_logs collection")
        
        # Wishlist collection indexes
        wishlist_collection = get_wishlist_collection()
        wishlist_collection.create_index("id", unique=True)
        wishlist_collection.create_index("user_id")
        wishlist_collection.create_index("item_id")
        print("   ✅ Created indexes for wishlist collection")
        
    except Exception as e:
        print(f"   ⚠️  Error creating indexes: {e}")

def main():
    """Main migration function"""
    print("🚀 Starting migration from JSON files to MongoDB...")
    print(f"📊 Target Database: {mongo_db.db.name}")
    
    # Test connection first
    if not mongo_db.client:
        print("❌ Failed to connect to MongoDB. Please check your connection string.")
        return
    
    # Migration mapping
    migrations = [
        ('data/users.json', 'users', 'Users'),
        ('data/items.json', 'items', 'Items'),
        ('data/exchanges.json', 'exchanges', 'Exchanges'),
        ('data/activity_logs.json', 'activity_logs', 'Activity Logs'),
        ('data/wishlist.json', 'wishlist', 'Wishlist')
    ]
    
    total_migrated = 0
    
    # Perform migrations
    for json_file, collection_name, description in migrations:
        count = migrate_collection(json_file, collection_name, description)
        total_migrated += count
    
    # Create indexes
    create_indexes()
    
    # Verify migration
    verify_migration()
    
    print(f"\n🎉 Migration completed! Total documents migrated: {total_migrated}")
    print("\n📋 Next steps:")
    print("   1. Update app.py to use MongoDB instead of JSON files")
    print("   2. Test the application with MongoDB")
    print("   3. Backup JSON files (they're no longer needed)")

if __name__ == "__main__":
    main()
