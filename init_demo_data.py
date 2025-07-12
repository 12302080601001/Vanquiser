#!/usr/bin/env python3
"""
Demo data initialization script for ReWear platform
Creates sample users, items, and exchanges for testing
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_demo_data():
    """Create demo data for the ReWear platform"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Demo users
    users = [
        {
            'id': str(uuid.uuid4()),
            'email': 'demo@rewear.com',
            'password': generate_password_hash('demo123'),
            'name': 'Demo User',
            'points': 150,
            'created_at': (datetime.now() - timedelta(days=30)).isoformat(),
            'is_admin': False
        },
        {
            'id': str(uuid.uuid4()),
            'email': 'admin@rewear.com',
            'password': generate_password_hash('admin123'),
            'name': 'Admin User',
            'points': 500,
            'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
            'is_admin': True
        },
        {
            'id': str(uuid.uuid4()),
            'email': 'sarah@example.com',
            'password': generate_password_hash('password123'),
            'name': 'Sarah Johnson',
            'points': 200,
            'created_at': (datetime.now() - timedelta(days=20)).isoformat(),
            'is_admin': False
        },
        {
            'id': str(uuid.uuid4()),
            'email': 'mike@example.com',
            'password': generate_password_hash('password123'),
            'name': 'Mike Chen',
            'points': 80,
            'created_at': (datetime.now() - timedelta(days=15)).isoformat(),
            'is_admin': False
        },
        {
            'id': str(uuid.uuid4()),
            'email': 'emma@example.com',
            'password': generate_password_hash('password123'),
            'name': 'Emma Wilson',
            'points': 120,
            'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
            'is_admin': False
        }
    ]
    
    # Demo items
    items = [
        {
            'id': str(uuid.uuid4()),
            'user_id': users[0]['id'],  # Demo user
            'title': 'Vintage Denim Jacket',
            'description': 'Classic blue denim jacket from the 90s. Slightly faded but in excellent condition. Perfect for layering. Brand: Levi\'s. 100% cotton.',
            'category': 'outerwear',
            'size': 'M',
            'condition': 'excellent',
            'points_value': 80,
            'image': 'uploads/default.jpg',
            'status': 'available',
            'created_at': (datetime.now() - timedelta(days=5)).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[2]['id'],  # Sarah
            'title': 'Floral Summer Dress',
            'description': 'Beautiful floral print dress perfect for summer. Lightweight fabric, midi length. Worn only a few times. Brand: Zara.',
            'category': 'dresses',
            'size': 'S',
            'condition': 'excellent',
            'points_value': 60,
            'image': 'uploads/default.jpg',
            'status': 'available',
            'created_at': (datetime.now() - timedelta(days=3)).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[3]['id'],  # Mike
            'title': 'Black Leather Boots',
            'description': 'Genuine leather ankle boots in black. Some wear on the soles but still in good condition. Great for fall/winter. Size 42 EU.',
            'category': 'shoes',
            'size': '42',
            'condition': 'good',
            'points_value': 70,
            'image': 'uploads/default.jpg',
            'status': 'available',
            'created_at': (datetime.now() - timedelta(days=7)).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[4]['id'],  # Emma
            'title': 'Cashmere Scarf',
            'description': 'Luxurious cashmere scarf in cream color. Super soft and warm. Perfect accessory for winter. Barely used.',
            'category': 'accessories',
            'size': 'One Size',
            'condition': 'excellent',
            'points_value': 45,
            'image': 'uploads/default.jpg',
            'status': 'available',
            'created_at': (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[1]['id'],  # Admin
            'title': 'Striped Cotton T-Shirt',
            'description': 'Classic navy and white striped t-shirt. 100% organic cotton. Comfortable fit. Brand: Uniqlo. Machine washable.',
            'category': 'tops',
            'size': 'L',
            'condition': 'good',
            'points_value': 25,
            'image': 'uploads/default.jpg',
            'status': 'available',
            'created_at': (datetime.now() - timedelta(days=8)).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'user_id': users[2]['id'],  # Sarah
            'title': 'High-Waisted Jeans',
            'description': 'Trendy high-waisted jeans in dark wash. Skinny fit. Great condition with minimal wear. Brand: H&M.',
            'category': 'bottoms',
            'size': 'M',
            'condition': 'excellent',
            'points_value': 50,
            'image': 'uploads/default.jpg',
            'status': 'exchanged',
            'created_at': (datetime.now() - timedelta(days=12)).isoformat()
        }
    ]
    
    # Demo exchanges
    exchanges = [
        {
            'id': str(uuid.uuid4()),
            'item_id': items[5]['id'],  # High-waisted jeans
            'requester_id': users[0]['id'],  # Demo user
            'owner_id': users[2]['id'],  # Sarah
            'points': 50,
            'status': 'completed',
            'created_at': (datetime.now() - timedelta(days=1)).isoformat()
        }
    ]
    
    # Save data to JSON files
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    with open('data/items.json', 'w') as f:
        json.dump(items, f, indent=2)
    
    with open('data/exchanges.json', 'w') as f:
        json.dump(exchanges, f, indent=2)
    
    print("✅ Demo data created successfully!")
    print("\n📋 Demo Accounts:")
    print("👤 Regular User: demo@rewear.com / demo123")
    print("🔧 Admin User: admin@rewear.com / admin123")
    print("👥 Other Users: sarah@example.com, mike@example.com, emma@example.com / password123")
    print(f"\n📊 Created:")
    print(f"   • {len(users)} users")
    print(f"   • {len(items)} items")
    print(f"   • {len(exchanges)} exchanges")

if __name__ == '__main__':
    create_demo_data()
