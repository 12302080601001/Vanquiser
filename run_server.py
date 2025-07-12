#!/usr/bin/env python3
"""
Universal server runner for ReWear application
Works on both Windows (development) and Linux (production)
"""
import os
import sys
import platform

def run_server():
    """Run the server with the appropriate method for the platform"""
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print(f"🚀 Starting ReWear server on {host}:{port}")
    print(f"🖥️  Platform: {platform.system()}")
    print(f"🐍 Python: {sys.version}")
    
    # Try to use gunicorn on Linux (production)
    if platform.system() == 'Linux':
        try:
            print("🔧 Attempting to use Gunicorn (production mode)...")
            import gunicorn.app.wsgiapp as wsgi
            
            # Configure gunicorn
            sys.argv = [
                'gunicorn',
                '--bind', f'{host}:{port}',
                '--workers', '1',
                '--timeout', '120',
                '--access-logfile', '-',
                '--error-logfile', '-',
                'app:app'
            ]
            
            wsgi.run()
            return
            
        except ImportError:
            print("⚠️  Gunicorn not available, falling back to Flask dev server")
        except Exception as e:
            print(f"⚠️  Gunicorn failed: {e}, falling back to Flask dev server")
    
    # Try to use waitress (cross-platform)
    try:
        print("🔧 Attempting to use Waitress (cross-platform mode)...")
        from waitress import serve
        from app import app
        
        print(f"✅ Starting Waitress server on {host}:{port}")
        serve(app, host=host, port=port, threads=4)
        return
        
    except ImportError:
        print("⚠️  Waitress not available, falling back to Flask dev server")
    except Exception as e:
        print(f"⚠️  Waitress failed: {e}, falling back to Flask dev server")
    
    # Fallback to Flask development server
    try:
        print("🔧 Using Flask development server (fallback mode)...")
        from app import app
        
        # Set production settings
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        print(f"✅ Starting Flask server on {host}:{port}")
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except Exception as e:
        print(f"❌ All server options failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_server()
