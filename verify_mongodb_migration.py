#!/usr/bin/env python3
"""
Verification script to ensure MongoDB migration is complete and working
"""
from database import (
    mongo_db, find_documents, find_one_document, count_documents,
    get_user_by_email, get_user_by_id, get_user_items, get_user_exchanges,
    get_user_activities, get_user_wishlist
)

def test_database_connection():
    """Test MongoDB connection"""
    print("🔗 Testing MongoDB Connection...")
    try:
        if mongo_db.client:
            mongo_db.client.admin.command('ping')
            print("   ✅ MongoDB connection successful")
            return True
        else:
            print("   ❌ MongoDB connection failed")
            return False
    except Exception as e:
        print(f"   ❌ MongoDB connection error: {e}")
        return False

def test_collections():
    """Test all collections exist and have data"""
    print("\n📊 Testing Collections...")
    
    collections = ['users', 'items', 'exchanges', 'activity_logs', 'wishlist']
    all_good = True
    
    for collection in collections:
        try:
            count = count_documents(collection)
            status = "✅" if count >= 0 else "❌"
            print(f"   {status} {collection}: {count} documents")
            
            if collection in ['users', 'items', 'exchanges', 'activity_logs'] and count == 0:
                print(f"      ⚠️  Warning: {collection} collection is empty")
                all_good = False
                
        except Exception as e:
            print(f"   ❌ Error accessing {collection}: {e}")
            all_good = False
    
    return all_good

def test_user_functions():
    """Test user-related functions"""
    print("\n👤 Testing User Functions...")
    
    try:
        # Test get_user_by_email
        users = find_documents('users')
        if users:
            test_user = users[0]
            user = get_user_by_email(test_user['email'])
            if user:
                print(f"   ✅ get_user_by_email: Found user {user['name']}")
                
                # Test get_user_by_id
                user_by_id = get_user_by_id(user['id'])
                if user_by_id:
                    print(f"   ✅ get_user_by_id: Found user {user_by_id['name']}")
                    
                    # Test user items
                    user_items = get_user_items(user['id'])
                    print(f"   ✅ get_user_items: Found {len(user_items)} items")
                    
                    # Test user exchanges
                    user_exchanges = get_user_exchanges(user['id'])
                    print(f"   ✅ get_user_exchanges: Found {len(user_exchanges)} exchanges")
                    
                    # Test user activities
                    user_activities = get_user_activities(user['id'])
                    print(f"   ✅ get_user_activities: Found {len(user_activities)} activities")
                    
                    # Test user wishlist
                    user_wishlist = get_user_wishlist(user['id'])
                    print(f"   ✅ get_user_wishlist: Found {len(user_wishlist)} wishlist items")
                    
                    return True
                else:
                    print("   ❌ get_user_by_id failed")
            else:
                print("   ❌ get_user_by_email failed")
        else:
            print("   ⚠️  No users found in database")
            
    except Exception as e:
        print(f"   ❌ Error testing user functions: {e}")
        
    return False

def test_data_integrity():
    """Test data integrity and relationships"""
    print("\n🔍 Testing Data Integrity...")
    
    try:
        users = find_documents('users')
        items = find_documents('items')
        exchanges = find_documents('exchanges')
        activities = find_documents('activity_logs')
        
        print(f"   📊 Data Summary:")
        print(f"      - Users: {len(users)}")
        print(f"      - Items: {len(items)}")
        print(f"      - Exchanges: {len(exchanges)}")
        print(f"      - Activities: {len(activities)}")
        
        # Check if items have valid user_ids
        valid_user_ids = {user['id'] for user in users}
        invalid_items = [item for item in items if item['user_id'] not in valid_user_ids]
        
        if invalid_items:
            print(f"   ⚠️  Found {len(invalid_items)} items with invalid user_ids")
        else:
            print("   ✅ All items have valid user_ids")
        
        # Check if exchanges have valid user_ids
        invalid_exchanges = []
        for exchange in exchanges:
            if (exchange.get('requester_id') not in valid_user_ids or 
                exchange.get('owner_id') not in valid_user_ids):
                invalid_exchanges.append(exchange)
        
        if invalid_exchanges:
            print(f"   ⚠️  Found {len(invalid_exchanges)} exchanges with invalid user_ids")
        else:
            print("   ✅ All exchanges have valid user_ids")
        
        # Check if activities have valid user_ids
        invalid_activities = [activity for activity in activities if activity['user_id'] not in valid_user_ids]
        
        if invalid_activities:
            print(f"   ⚠️  Found {len(invalid_activities)} activities with invalid user_ids")
        else:
            print("   ✅ All activities have valid user_ids")
        
        return len(invalid_items) == 0 and len(invalid_exchanges) == 0 and len(invalid_activities) == 0
        
    except Exception as e:
        print(f"   ❌ Error testing data integrity: {e}")
        return False

def test_admin_user():
    """Test admin user exists"""
    print("\n👑 Testing Admin User...")
    
    try:
        admin = get_user_by_email('admin@rewear.com')
        if admin and admin.get('is_admin', False):
            print("   ✅ Admin user exists and has admin privileges")
            print(f"      - Name: {admin['name']}")
            print(f"      - Email: {admin['email']}")
            print(f"      - Points: {admin['points']}")
            return True
        else:
            print("   ❌ Admin user not found or lacks admin privileges")
            return False
    except Exception as e:
        print(f"   ❌ Error testing admin user: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 MongoDB Migration Verification")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Collections", test_collections),
        ("User Functions", test_user_functions),
        ("Data Integrity", test_data_integrity),
        ("Admin User", test_admin_user)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MongoDB migration is successful!")
        print("\n✅ Your ReWear application is ready to use with MongoDB!")
        print("\n📋 Next steps:")
        print("   1. Test the web application at http://127.0.0.1:5000")
        print("   2. Login with admin@rewear.com / admin123")
        print("   3. Test all dashboard features")
        print("   4. Deploy to Render with MongoDB configuration")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        
    return passed == total

if __name__ == "__main__":
    main()
