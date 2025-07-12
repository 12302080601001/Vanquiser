#!/usr/bin/env python3
"""
Deployment verification script
"""
import sys
import os

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'flask',
        'flask_mail',
        'gunicorn',
        'pymongo',
        'dnspython',
        'werkzeug',
        'jinja2'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All dependencies available!")
        return True

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'MAIL_SERVER',
        'MAIL_USERNAME',
        'MAIL_PASSWORD'
    ]
    
    missing = []
    for var in required_vars:
        if os.getenv(var):
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ {var}")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing)}")
        print("   These will be set by Render during deployment")
    else:
        print("\n✅ All environment variables set!")
    
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    
    required_files = [
        'app.py',
        'database.py',
        'requirements.txt',
        'Procfile',
        'render.yaml',
        'startup.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All required files present!")
        return True

def test_app_import():
    """Test if the app can be imported"""
    print("\n🔍 Testing app import...")
    
    try:
        from app import app
        print("   ✅ App imported successfully!")
        return True
    except Exception as e:
        print(f"   ❌ App import failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🚀 Deployment Verification")
    print("=" * 50)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Files", check_files),
        ("App Import", test_app_import)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        if check_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Ready for deployment!")
    else:
        print("⚠️  Some issues found. Please fix before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
