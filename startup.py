#!/usr/bin/env python3
"""
Startup script to ensure all necessary directories and MongoDB connection exist
"""
import os
import json
from database import mongo_db, insert_document, find_one_document

def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'data',
        'static',
        'static/uploads',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")

def ensure_data_files():
    """Create empty data files if they don't exist"""
    data_files = {
        'data/users.json': [],
        'data/items.json': [],
        'data/exchanges.json': [],
        'data/activity_logs.json': [],
        'data/wishlist.json': []
    }
    
    for file_path, default_content in data_files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(default_content, f, indent=2)
            print(f"Created data file: {file_path}")

def create_admin_user():
    """Create default admin user if no users exist in MongoDB"""
    try:
        # Check if admin user exists in MongoDB
        admin_user = find_one_document('users', {'email': 'admin@rewear.com'})

        if not admin_user:
            from werkzeug.security import generate_password_hash
            import uuid
            from datetime import datetime

            admin_user = {
                'id': str(uuid.uuid4()),
                'email': 'admin@rewear.com',
                'password': generate_password_hash('admin123'),
                'name': 'Admin User',
                'points': 1000,
                'created_at': datetime.now().isoformat(),
                'is_admin': True
            }

            insert_document('users', admin_user)

            print("Created default admin user:")
            print("Email: admin@rewear.com")
            print("Password: admin123")
            print("Please change the password after first login!")
        else:
            print("Admin user already exists in MongoDB")
    except Exception as e:
        print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    print("Running startup script...")

    # Test MongoDB connection
    if not mongo_db.client:
        print("❌ Failed to connect to MongoDB. Please check your connection.")
        exit(1)

    ensure_directories()
    ensure_data_files()
    create_admin_user()
    print("Startup script completed!")
