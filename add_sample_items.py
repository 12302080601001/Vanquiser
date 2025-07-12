#!/usr/bin/env python3
"""
Add sample items to MongoDB for testing
"""
import uuid
from datetime import datetime
from database import insert_document, find_documents

def add_sample_items():
    """Add sample fashion items to the database"""
    
    # Get existing users to assign items to
    users = find_documents('users')
    if not users:
        print("❌ No users found. Please run the migration first.")
        return
    
    # Sample items data
    sample_items = [
        {
            'id': str(uuid.uuid4()),
            'user_id': users[0]['id'],  # Assign to first user
            'title': 'Vintage Denim Jacket',
            'description': 'Classic blue denim jacket in excellent condition. Perfect for casual outings.',
            'category': 'outerwear',
            'size': 'M',
            'condition': 'excellent',
            'points_value': 25,
            'status': 'available',
            'image': 'static/uploads/default.jpg',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[1]['id'] if len(users) > 1 else users[0]['id'],
            'title': 'Floral Summer Dress',
            'description': 'Beautiful floral print dress, perfect for summer occasions.',
            'category': 'dresses',
            'size': 'S',
            'condition': 'good',
            'points_value': 20,
            'status': 'available',
            'image': 'static/uploads/default.jpg',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[2]['id'] if len(users) > 2 else users[0]['id'],
            'title': 'Black Leather Boots',
            'description': 'Stylish black leather boots, barely worn. Great for winter.',
            'category': 'shoes',
            'size': '8',
            'condition': 'excellent',
            'points_value': 30,
            'status': 'available',
            'image': 'static/uploads/default.jpg',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[3]['id'] if len(users) > 3 else users[0]['id'],
            'title': 'Cotton T-Shirt',
            'description': 'Comfortable white cotton t-shirt, perfect for everyday wear.',
            'category': 'tops',
            'size': 'L',
            'condition': 'good',
            'points_value': 15,
            'status': 'available',
            'image': 'static/uploads/default.jpg',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[4]['id'] if len(users) > 4 else users[0]['id'],
            'title': 'Designer Handbag',
            'description': 'Elegant designer handbag in mint condition. Perfect for special occasions.',
            'category': 'accessories',
            'size': 'One Size',
            'condition': 'excellent',
            'points_value': 40,
            'status': 'available',
            'image': 'static/uploads/default.jpg',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[0]['id'],  # Give first user multiple items
            'title': 'Blue Jeans',
            'description': 'Classic blue jeans, comfortable fit. Great for casual wear.',
            'category': 'bottoms',
            'size': '32',
            'condition': 'good',
            'points_value': 18,
            'status': 'available',
            'image': 'static/uploads/default.jpg',
            'created_at': datetime.now().isoformat()
        }
    ]
    
    print("📦 Adding sample items to MongoDB...")
    
    # Check if items already exist
    existing_items = find_documents('items')
    if existing_items:
        print(f"⚠️  Found {len(existing_items)} existing items")
        response = input("🤔 Do you want to add more sample items? (y/N): ").lower()
        if response != 'y':
            print("⏭️  Skipping sample items addition")
            return
    
    # Insert sample items
    inserted_count = 0
    for item in sample_items:
        try:
            insert_document('items', item)
            inserted_count += 1
            print(f"   ✅ Added: {item['title']} (Category: {item['category']})")
        except Exception as e:
            print(f"   ❌ Failed to add {item['title']}: {e}")
    
    print(f"\n🎉 Successfully added {inserted_count} sample items!")
    
    # Show summary
    total_items = len(find_documents('items'))
    print(f"📊 Total items in database: {total_items}")
    
    # Show items by category
    categories = {}
    for item in find_documents('items'):
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📋 Items by category:")
    for category, count in categories.items():
        print(f"   - {category.title()}: {count} items")

if __name__ == "__main__":
    add_sample_items()
