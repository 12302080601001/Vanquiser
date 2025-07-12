#!/usr/bin/env python3
"""
Final deployment verification script
"""
import sys
import platform

def verify_deployment():
    """Verify all deployment components are ready"""
    print("🔍 Final Deployment Verification")
    print("=" * 50)
    
    issues = []
    
    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        issues.append("Python version should be 3.8+")
    else:
        print("   ✅ Python version compatible")
    
    # Check required modules
    required_modules = [
        ('flask', 'Flask web framework'),
        ('pymongo', 'MongoDB driver'),
        ('gunicorn', 'WSGI server (Linux)'),
        ('waitress', 'WSGI server (cross-platform)'),
        ('werkzeug', 'WSGI utilities'),
        ('jinja2', 'Template engine'),
        ('flask_mail', 'Email functionality')
    ]
    
    print("\n📦 Checking Dependencies:")
    for module, description in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module} - {description}")
        except ImportError:
            print(f"   ❌ {module} - {description}")
            issues.append(f"Missing module: {module}")
    
    # Check files
    required_files = [
        ('app.py', 'Main application'),
        ('database.py', 'Database functions'),
        ('run_server.py', 'Universal server runner'),
        ('requirements.txt', 'Dependencies'),
        ('render.yaml', 'Render configuration'),
        ('Procfile', 'Process configuration'),
        ('startup.py', 'Initialization script')
    ]
    
    print("\n📁 Checking Files:")
    import os
    for filename, description in required_files:
        if os.path.exists(filename):
            print(f"   ✅ {filename} - {description}")
        else:
            print(f"   ❌ {filename} - {description}")
            issues.append(f"Missing file: {filename}")
    
    # Check server runner
    print("\n🚀 Testing Server Runner:")
    try:
        from run_server import run_server
        print("   ✅ Server runner imports successfully")
    except Exception as e:
        print(f"   ❌ Server runner error: {e}")
        issues.append("Server runner import failed")
    
    # Check app import
    print("\n🌐 Testing App Import:")
    try:
        from app import app
        print("   ✅ Flask app imports successfully")
    except Exception as e:
        print(f"   ❌ App import error: {e}")
        issues.append("Flask app import failed")
    
    # Check database connection
    print("\n🗄️  Testing Database:")
    try:
        from database import mongo_db
        if mongo_db.client:
            print("   ✅ MongoDB connection available")
        else:
            print("   ⚠️  MongoDB connection not established")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        issues.append("Database connection failed")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Verification Summary:")
    
    if not issues:
        print("🎉 ALL CHECKS PASSED!")
        print("\n✅ Your ReWear application is ready for deployment!")
        print("\n🚀 Deployment Steps:")
        print("   1. Commit all changes to your repository")
        print("   2. Push to GitHub/GitLab")
        print("   3. Deploy to Render")
        print("   4. Monitor deployment logs")
        print("   5. Test the live application")
        print("\n🌍 Expected Success:")
        print("   - Build successful")
        print("   - Server starts with run_server.py")
        print("   - MongoDB connection established")
        print("   - All features functional")
        return True
    else:
        print(f"⚠️  Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n🔧 Please fix these issues before deploying")
        return False

if __name__ == "__main__":
    success = verify_deployment()
    sys.exit(0 if success else 1)
