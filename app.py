from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import uuid
import threading
from dotenv import load_dotenv
from database import (
    get_user_by_email, get_user_by_id, get_user_items, get_user_exchanges,
    get_user_activities, get_user_wishlist, insert_document, find_documents,
    find_one_document, update_document, delete_document, count_documents
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'rewear_secret_key_2024')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB max file size

# Email Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'mkbharvad534@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'dwtp fmiq miyl ccvq')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'mkbharvad534@gmail.com')

# Initialize Flask-Mail
mail = Mail(app)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MongoDB Database (replacing JSON files)
# Collections: users, items, exchanges, activity_logs, wishlist

# Create data directory for backward compatibility (file uploads, etc.)
os.makedirs('data', exist_ok=True)

# Initialize application
def initialize_app():
    """Initialize the application"""
    try:
        from startup import ensure_directories, create_admin_user
        print("🚀 Initializing ReWear application...")
        ensure_directories()
        create_admin_user()
        print("✅ Application initialized successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Application initialization warning: {e}")
        # Continue anyway - the app can still function
        return False

# Global flag to track initialization
_app_initialized = False

# Legacy functions - now using MongoDB
def load_data(collection_name):
    """Load data from MongoDB collection (replaces JSON file loading)"""
    return find_documents(collection_name)

def save_data(collection_name, data):
    """Save data to MongoDB collection (replaces JSON file saving)"""
    # This function is deprecated - use insert_document, update_document instead
    pass

# get_user_by_email is now imported from database.py

# get_user_by_id is now imported from database.py

@app.context_processor
def inject_user():
    return dict(get_user_by_id=get_user_by_id)

# Activity Logging Functions
def log_activity(user_id, action, details, ip_address=None):
    """Log user activity for admin monitoring"""
    try:
        new_log = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'action': action,
            'details': details,
            'ip_address': ip_address or request.remote_addr if request else 'Unknown',
            'timestamp': datetime.now().isoformat(),
            'user_agent': request.headers.get('User-Agent', 'Unknown') if request else 'Unknown'
        }
        insert_document('activity_logs', new_log)
        return True
    except Exception as e:
        print(f"Failed to log activity: {str(e)}")
        return False

# get_user_activities is now imported from database.py

def get_all_activities(limit=100):
    """Get recent activities for all users"""
    activities = find_documents('activity_logs')
    return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:limit]

def get_activity_stats():
    """Get activity statistics for admin dashboard"""
    logs = find_documents('activity_logs')
    today = datetime.now().date()

    stats = {
        'total_activities': len(logs),
        'today_activities': len([log for log in logs if datetime.fromisoformat(log['timestamp']).date() == today]),
        'unique_users_today': len(set([log['user_id'] for log in logs if datetime.fromisoformat(log['timestamp']).date() == today])),
        'most_active_users': {},
        'popular_actions': {}
    }

    # Count activities by user
    user_activity_count = {}
    action_count = {}

    for log in logs:
        user_id = log['user_id']
        action = log['action']

        user_activity_count[user_id] = user_activity_count.get(user_id, 0) + 1
        action_count[action] = action_count.get(action, 0) + 1

    # Get top 5 most active users
    sorted_users = sorted(user_activity_count.items(), key=lambda x: x[1], reverse=True)[:5]
    for user_id, count in sorted_users:
        user = get_user_by_id(user_id)
        if user:
            stats['most_active_users'][user['name']] = count

    # Get top 5 popular actions
    sorted_actions = sorted(action_count.items(), key=lambda x: x[1], reverse=True)[:5]
    stats['popular_actions'] = dict(sorted_actions)

    return stats

# Email Functions
def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
            print(f"Email sent successfully to {msg.recipients}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

def send_email(subject, recipients, html_body, text_body=None):
    """Send email with HTML and optional text body"""
    try:
        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            html=html_body,
            body=text_body or "Please view this email in HTML format."
        )

        # Send email in background thread
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
        return True
    except Exception as e:
        print(f"Error creating email: {str(e)}")
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    subject = "🎉 Welcome to ReWear - Your Sustainable Fashion Journey Begins!"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; }}
            .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
            .btn {{ background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 10px 0; }}
            .points-badge {{ background: linear-gradient(45deg, #ff9a9e, #fecfef); color: #333; padding: 8px 16px; border-radius: 20px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌟 Welcome to ReWear!</h1>
                <p>Your Sustainable Fashion Journey Starts Here</p>
            </div>
            <div class="content">
                <h2>Hello {user['name']}! 👋</h2>
                <p>Thank you for joining ReWear, the community-driven platform for sustainable fashion exchange!</p>

                <h3>🎁 Your Welcome Gift:</h3>
                <p>We've credited your account with <span class="points-badge">100 Points</span> to get you started!</p>

                <h3>🚀 What You Can Do:</h3>
                <ul>
                    <li>📸 <strong>Upload Items:</strong> Share your unused clothing with the community</li>
                    <li>🔍 <strong>Browse & Discover:</strong> Find unique fashion pieces from other users</li>
                    <li>🔄 <strong>Exchange:</strong> Trade items using our points system</li>
                    <li>🌱 <strong>Go Green:</strong> Reduce textile waste and promote sustainability</li>
                </ul>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/dashboard" class="btn">Visit Your Dashboard</a>
                </div>

                <h3>📧 Email Notifications:</h3>
                <p>You'll receive email updates for:</p>
                <ul>
                    <li>✅ Item upload confirmations</li>
                    <li>✅ Exchange requests and completions</li>
                    <li>✅ Points earned and spent</li>
                    <li>✅ Platform updates and tips</li>
                </ul>

                <p>Happy exchanging! 🎉</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Making Sustainable Fashion Accessible to Everyone</p>
                <p>🌍 Reduce • Reuse • ReWear ♻️</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, user['email'], html_body)

def send_login_email(user):
    """Send login notification email"""
    subject = f"👋 Welcome back to ReWear, {user['name']}!"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            .btn {{ background: linear-gradient(45deg, #4ecdc4, #44a08d); color: white; padding: 10px 25px; text-decoration: none; border-radius: 25px; display: inline-block; }}
            .points-display {{ background: linear-gradient(45deg, #ff9a9e, #fecfef); color: #333; padding: 15px; border-radius: 10px; text-align: center; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Welcome Back! 🎉</h2>
            </div>
            <div class="content">
                <p>Hi {user['name']},</p>
                <p>You've successfully logged into your ReWear account!</p>

                <div class="points-display">
                    <h3>💰 Your Current Balance</h3>
                    <h2>{user['points']} Points</h2>
                </div>

                <p>Ready to continue your sustainable fashion journey?</p>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:5000/browse" class="btn">Browse Items</a>
                    <a href="http://localhost:5000/upload" class="btn">Upload Item</a>
                </div>

                <p>Happy exchanging!</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Sustainable Fashion Exchange</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, user['email'], html_body)

def send_item_upload_email(user, item):
    """Send email notification when user uploads an item"""
    subject = f"📸 Item Upload Successful - {item['title']}"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); color: white; padding: 25px; text-align: center; }}
            .content {{ padding: 25px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            .item-card {{ border: 1px solid #dee2e6; border-radius: 10px; padding: 20px; margin: 15px 0; background-color: #f8f9fa; }}
            .btn {{ background: linear-gradient(45deg, #feca57, #ff9ff3); color: white; padding: 10px 25px; text-decoration: none; border-radius: 25px; display: inline-block; }}
            .points-badge {{ background: linear-gradient(45deg, #ff9a9e, #fecfef); color: #333; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🎉 Item Upload Successful!</h2>
            </div>
            <div class="content">
                <p>Hi {user['name']},</p>
                <p>Your item has been successfully uploaded to ReWear! 🎊</p>

                <div class="item-card">
                    <h3>📦 Item Details:</h3>
                    <p><strong>Title:</strong> {item['title']}</p>
                    <p><strong>Category:</strong> {item['category'].title()}</p>
                    <p><strong>Size:</strong> {item['size']}</p>
                    <p><strong>Condition:</strong> {item['condition'].title()}</p>
                    <p><strong>Points Value:</strong> <span class="points-badge">{item['points_value']} Points</span></p>
                    <p><strong>Description:</strong> {item['description'][:100]}{'...' if len(item['description']) > 100 else ''}</p>
                </div>

                <h3>🚀 What's Next?</h3>
                <ul>
                    <li>✅ Your item is now live and visible to all users</li>
                    <li>🔍 Other users can discover and exchange your item</li>
                    <li>📧 You'll get notified when someone requests an exchange</li>
                    <li>💰 Earn {item['points_value']} points when your item is exchanged</li>
                </ul>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:5000/item/{item['id']}" class="btn">View Your Item</a>
                    <a href="http://localhost:5000/dashboard" class="btn">Go to Dashboard</a>
                </div>

                <p>Thank you for contributing to sustainable fashion! 🌱</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Every Upload Makes a Difference</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, user['email'], html_body)

def send_exchange_request_email(owner, requester, item):
    """Send email to item owner when someone requests an exchange"""
    subject = f"🔄 Exchange Request for '{item['title']}'"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #54a0ff 0%, #5f27cd 100%); color: white; padding: 25px; text-align: center; }}
            .content {{ padding: 25px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            .exchange-card {{ border: 2px solid #54a0ff; border-radius: 10px; padding: 20px; margin: 15px 0; background-color: #f0f8ff; }}
            .btn {{ background: linear-gradient(45deg, #54a0ff, #5f27cd); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 5px; }}
            .points-badge {{ background: linear-gradient(45deg, #ff9a9e, #fecfef); color: #333; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🎉 Exchange Request Received!</h2>
            </div>
            <div class="content">
                <p>Hi {owner['name']},</p>
                <p>Great news! Someone wants to exchange your item! 🎊</p>

                <div class="exchange-card">
                    <h3>📦 Exchange Details:</h3>
                    <p><strong>Your Item:</strong> {item['title']}</p>
                    <p><strong>Requested by:</strong> {requester['name']}</p>
                    <p><strong>Points to Earn:</strong> <span class="points-badge">{item['points_value']} Points</span></p>
                    <p><strong>Exchange Status:</strong> ✅ Completed Automatically</p>
                </div>

                <h3>🎉 Congratulations!</h3>
                <ul>
                    <li>💰 You've earned <strong>{item['points_value']} points</strong></li>
                    <li>🌱 You've contributed to sustainable fashion</li>
                    <li>♻️ Your item found a new loving home</li>
                    <li>🎯 You can use your points to get new items</li>
                </ul>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:5000/dashboard" class="btn">View Dashboard</a>
                    <a href="http://localhost:5000/browse" class="btn">Browse More Items</a>
                </div>

                <p>Thank you for being part of the ReWear community! 🌟</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Connecting Fashion Lovers Sustainably</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, owner['email'], html_body)

def send_exchange_success_email(requester, owner, item):
    """Send email to requester when exchange is successful"""
    subject = f"🎉 Exchange Successful - You got '{item['title']}'!"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #00d2d3 0%, #54a0ff 100%); color: white; padding: 25px; text-align: center; }}
            .content {{ padding: 25px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            .success-card {{ border: 2px solid #00d2d3; border-radius: 10px; padding: 20px; margin: 15px 0; background-color: #f0ffff; }}
            .btn {{ background: linear-gradient(45deg, #00d2d3, #54a0ff); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 5px; }}
            .points-badge {{ background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🎊 Exchange Completed Successfully!</h2>
            </div>
            <div class="content">
                <p>Hi {requester['name']},</p>
                <p>Congratulations! Your exchange request has been completed! 🎉</p>

                <div class="success-card">
                    <h3>🎁 Your New Item:</h3>
                    <p><strong>Item:</strong> {item['title']}</p>
                    <p><strong>From:</strong> {owner['name']}</p>
                    <p><strong>Points Spent:</strong> <span class="points-badge">{item['points_value']} Points</span></p>
                    <p><strong>Category:</strong> {item['category'].title()}</p>
                    <p><strong>Size:</strong> {item['size']}</p>
                    <p><strong>Condition:</strong> {item['condition'].title()}</p>
                </div>

                <h3>🌟 What's Next?</h3>
                <ul>
                    <li>📧 Contact details will be shared separately for pickup/delivery</li>
                    <li>💰 Your remaining balance: Check your dashboard</li>
                    <li>📸 Consider uploading more items to earn points</li>
                    <li>🔍 Continue browsing for more amazing finds</li>
                </ul>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:5000/dashboard" class="btn">View Dashboard</a>
                    <a href="http://localhost:5000/upload" class="btn">Upload Item</a>
                </div>

                <p>Enjoy your new sustainable fashion find! 🌱</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Sustainable Fashion Exchange</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, requester['email'], html_body)

def send_daily_activity_email(user, activities):
    """Send daily activity summary email"""
    subject = f"📊 Your ReWear Daily Summary - {datetime.now().strftime('%B %d, %Y')}"

    activity_html = ""
    for activity in activities:
        activity_html += f"<li>✅ {activity}</li>"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            .activity-list {{ background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; }}
            .btn {{ background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 10px 25px; text-decoration: none; border-radius: 25px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>📊 Your Daily ReWear Summary</h2>
            </div>
            <div class="content">
                <p>Hi {user['name']},</p>
                <p>Here's what happened in your ReWear account today:</p>

                <div class="activity-list">
                    <h3>🎯 Today's Activities:</h3>
                    <ul>
                        {activity_html}
                    </ul>
                </div>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:5000/dashboard" class="btn">View Dashboard</a>
                </div>

                <p>Keep up the great work with sustainable fashion! 🌱</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Your Daily Fashion Impact</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, user['email'], html_body)

def send_points_update_email(user, points_change, reason):
    """Send email when user's points change"""
    subject = f"💰 Points Update - {'+' if points_change > 0 else ''}{points_change} Points"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
            .header {{ background: linear-gradient(135deg, {'#28a745' if points_change > 0 else '#dc3545'} 0%, {'#20c997' if points_change > 0 else '#e74c3c'} 100%); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #6c757d; }}
            .points-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; margin: 15px 0; }}
            .btn {{ background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 10px 25px; text-decoration: none; border-radius: 25px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>💰 Points {'Earned' if points_change > 0 else 'Spent'}!</h2>
            </div>
            <div class="content">
                <p>Hi {user['name']},</p>
                <p>Your points balance has been updated!</p>

                <div class="points-card">
                    <h3>{'🎉' if points_change > 0 else '💸'} {'+' if points_change > 0 else ''}{points_change} Points</h3>
                    <p><strong>Reason:</strong> {reason}</p>
                    <p><strong>Current Balance:</strong> {user['points']} Points</p>
                </div>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://localhost:5000/browse" class="btn">Browse Items</a>
                </div>

                <p>{'Great job contributing to sustainable fashion!' if points_change > 0 else 'Enjoy your new item!'}</p>
                <p><strong>The ReWear Team</strong></p>
            </div>
            <div class="footer">
                <p>ReWear - Every Point Counts</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(subject, user['email'], html_body)

@app.route('/')
def home():
    # Initialize app on first access
    global _app_initialized
    if not _app_initialized:
        initialize_app()
        _app_initialized = True

    # Get latest 6 available items for homepage
    items = find_documents('items', {'status': 'available'})
    latest_items = sorted(items, key=lambda x: x['created_at'], reverse=True)[:6]
    return render_template('index.html', items=latest_items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        if not email or not password or not name:
            flash('Please fill in all fields!', 'error')
            return render_template('register.html')

        if get_user_by_email(email):
            flash('Email already exists! Please use a different email.', 'error')
            return render_template('register.html')

        new_user = {
            'id': str(uuid.uuid4()),
            'email': email,
            'password': generate_password_hash(password),
            'name': name,
            'points': 100,  # Starting points
            'created_at': datetime.now().isoformat(),
            'is_admin': False
        }
        insert_document('users', new_user)

        # Log activity
        log_activity(new_user['id'], 'REGISTER', f"New user {name} registered with email {email}")

        # Send welcome email
        send_welcome_email(new_user)

        flash(f'Welcome to ReWear, {name}! You have been given 100 starting points. Check your email for welcome message!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Please fill in all fields!', 'error')
            return render_template('login.html')

        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']

            # Log activity
            log_activity(user['id'], 'LOGIN', f"User {user['name']} logged in successfully")

            # Send login notification email
            send_login_email(user)

            flash(f'Welcome back, {user["name"]}! Check your email for login confirmation.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f'Goodbye {user_name}! You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login to view your profile.', 'error')
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('home'))

    user_items = get_user_items(user['id'])
    user_exchanges = get_user_exchanges(user['id'])

    return render_template('profile.html', user=user, items=user_items, exchanges=user_exchanges)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])

    # Get user data from MongoDB
    user_items = get_user_items(user['id'])
    user_exchanges = get_user_exchanges(user['id'])

    # Get user activity logs
    user_activities = get_user_activities(user['id'], 10)

    # Calculate user statistics
    user_stats = {
        'total_items': len(user_items),
        'available_items': len([item for item in user_items if item['status'] == 'available']),
        'exchanged_items': len([item for item in user_items if item['status'] == 'exchanged']),
        'total_exchanges': len(user_exchanges),
        'completed_exchanges': len([ex for ex in user_exchanges if ex['status'] == 'completed']),
        'points_earned': sum([ex['points'] for ex in user_exchanges if ex['owner_id'] == user['id'] and ex['status'] == 'completed']),
        'points_spent': sum([ex['points'] for ex in user_exchanges if ex['requester_id'] == user['id'] and ex['status'] == 'completed'])
    }

    # Get wishlist items
    user_wishlist = get_user_wishlist(user['id'])
    user_wishlist_ids = [w['item_id'] for w in user_wishlist]
    wishlist_items = find_documents('items', {'id': {'$in': user_wishlist_ids}}) if user_wishlist_ids else []

    return render_template('dashboard.html', user=user, items=user_items, exchanges=user_exchanges,
                         activities=user_activities, stats=user_stats, wishlist_items=wishlist_items)

@app.route('/browse')
def browse():
    # Get all available items from MongoDB
    query = {'status': 'available'}
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    if category:
        query['category'] = {'$regex': category, '$options': 'i'}

    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}}
        ]

    items = find_documents('items', query)
    
    return render_template('browse.html', items=items, category=category, search=search)

@app.route('/upload', methods=['GET', 'POST'])
def upload_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        size = request.form['size']
        condition = request.form['condition']
        points_value = int(request.form['points_value'])
        
        # Handle file upload
        file = request.files['image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"static/uploads/{filename}"
        else:
            image_path = "static/uploads/placeholder.jpg"  # This will trigger the onerror fallback
        
        new_item = {
            'id': str(uuid.uuid4()),
            'user_id': session['user_id'],
            'title': title,
            'description': description,
            'category': category,
            'size': size,
            'condition': condition,
            'points_value': points_value,
            'image': image_path,
            'status': 'available',
            'created_at': datetime.now().isoformat()
        }
        insert_document('items', new_item)

        # Log activity
        log_activity(session['user_id'], 'ITEM_UPLOAD', f"Uploaded item: {title} ({category}) for {points_value} points")

        # Send item upload email
        user = get_user_by_id(session['user_id'])
        if user:
            send_item_upload_email(user, new_item)

        flash('Item uploaded successfully! Check your email for confirmation.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('upload.html')

@app.route('/item/<item_id>')
def item_detail(item_id):
    item = find_one_document('items', {'id': item_id})

    if not item:
        flash('Item not found!', 'error')
        return redirect(url_for('browse'))
    
    # Get item owner info
    owner = get_user_by_id(item['user_id'])
    
    return render_template('item_detail.html', item=item, owner=owner)

@app.route('/request_exchange/<item_id>')
def request_exchange(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = get_user_by_id(session['user_id'])
    item = find_one_document('items', {'id': item_id})

    if not item or item['user_id'] == user['id']:
        flash('Invalid request!', 'error')
        return redirect(url_for('browse'))
    
    if user['points'] < item['points_value']:
        flash('Insufficient points!', 'error')
        return redirect(url_for('item_detail', item_id=item_id))
    
    # Process exchange
    new_exchange = {
        'id': str(uuid.uuid4()),
        'item_id': item_id,
        'requester_id': user['id'],
        'owner_id': item['user_id'],
        'points': item['points_value'],
        'status': 'completed',
        'created_at': datetime.now().isoformat()
    }
    insert_document('exchanges', new_exchange)

    # Update user points
    update_document('users', {'id': user['id']}, {'$inc': {'points': -item['points_value']}})
    update_document('users', {'id': item['user_id']}, {'$inc': {'points': item['points_value']}})

    # Update item status
    update_document('items', {'id': item_id}, {'$set': {'status': 'exchanged'}})

    # Log activity for both users
    log_activity(user['id'], 'ITEM_EXCHANGE_REQUEST', f"Requested exchange for item: {item['title']} (spent {item['points_value']} points)")
    log_activity(item['user_id'], 'ITEM_EXCHANGE_RECEIVED', f"Item exchanged: {item['title']} (earned {item['points_value']} points)")

    # Send email notifications
    owner = get_user_by_id(item['user_id'])
    requester = get_user_by_id(user['id'])

    if owner:
        send_exchange_request_email(owner, requester, item)
    if requester:
        send_exchange_success_email(requester, owner, item)

    flash('Exchange completed successfully! Check your email for confirmation.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/wishlist/add/<item_id>')
def add_to_wishlist(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401

    user = get_user_by_id(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if item exists
    item = find_one_document('items', {'id': item_id})
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    # Check if user owns the item
    if item['user_id'] == user['id']:
        return jsonify({'error': 'Cannot add your own item to wishlist'}), 400

    # Check if already in wishlist
    existing = find_one_document('wishlist', {'user_id': user['id'], 'item_id': item_id})
    if existing:
        return jsonify({'error': 'Item already in wishlist'}), 400

    # Add to wishlist
    new_wishlist_item = {
        'id': str(uuid.uuid4()),
        'user_id': user['id'],
        'item_id': item_id,
        'created_at': datetime.now().isoformat()
    }
    insert_document('wishlist', new_wishlist_item)

    # Log activity
    log_activity(user['id'], 'WISHLIST_ADD', f"Added item to wishlist: {item['title']}")

    return jsonify({'success': 'Item added to wishlist'})

@app.route('/wishlist/remove/<item_id>')
def remove_from_wishlist(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401

    user = get_user_by_id(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Remove from wishlist
    delete_document('wishlist', {'user_id': user['id'], 'item_id': item_id})

    # Log activity
    log_activity(user['id'], 'WISHLIST_REMOVE', f"Removed item from wishlist")

    return jsonify({'success': 'Item removed from wishlist'})

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('Please login to access admin panel.', 'error')
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('home'))

    if not user.get('is_admin'):
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('home'))

    users = find_documents('users')
    items = find_documents('items')
    exchanges = find_documents('exchanges')

    # Calculate statistics
    total_points = sum(user.get('points', 0) for user in users)
    active_items = len([item for item in items if item['status'] == 'available'])
    completed_exchanges = len([ex for ex in exchanges if ex['status'] == 'completed'])

    stats = {
        'total_users': len(users),
        'total_items': len(items),
        'active_items': active_items,
        'total_exchanges': len(exchanges),
        'completed_exchanges': completed_exchanges,
        'total_points': total_points
    }

    # Get activity logs and stats
    activity_logs = get_all_activities(50)
    activity_stats = get_activity_stats()

    return render_template('admin.html',
                         users=users,
                         items=items,
                         exchanges=exchanges,
                         stats=stats,
                         current_user=user,
                         activity_logs=activity_logs,
                         activity_stats=activity_stats)

@app.route('/admin/profile')
def admin_profile():
    """Admin profile page"""
    if 'user_id' not in session:
        flash('Please login to access admin profile.', 'error')
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])
    if not user or not user.get('is_admin'):
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('home'))

    # Get admin-specific data
    user_activities = get_user_activities(user['id'], 20)
    admin_stats = {
        'total_logins': len([log for log in user_activities if log['action'] == 'LOGIN']),
        'admin_actions': len([log for log in user_activities if 'ADMIN' in log['action']]),
        'last_login': user_activities[0]['timestamp'] if user_activities else 'Never',
        'account_created': user['created_at']
    }

    return render_template('admin_profile.html', user=user, activities=user_activities, admin_stats=admin_stats)

# AJAX Admin Routes
@app.route('/admin/api/users', methods=['GET'])
def admin_api_users():
    """API endpoint for user management"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = get_user_by_id(session['user_id'])
    if not user or not user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    users = find_documents('users')
    return jsonify({'users': users})

@app.route('/admin/api/user/<user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    """Delete user via API"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    admin_user = get_user_by_id(session['user_id'])
    if not admin_user or not admin_user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    user_to_delete = find_one_document('users', {'id': user_id})

    if not user_to_delete:
        return jsonify({'error': 'User not found'}), 404

    if user_to_delete.get('is_admin'):
        return jsonify({'error': 'Cannot delete admin user'}), 400

    # Remove user
    delete_document('users', {'id': user_id})

    # Log admin action
    log_activity(admin_user['id'], 'ADMIN_DELETE_USER', f"Deleted user: {user_to_delete['name']} ({user_to_delete['email']})")

    return jsonify({'success': True, 'message': 'User deleted successfully'})

@app.route('/admin/api/user/<user_id>/toggle-admin', methods=['POST'])
def admin_toggle_user_admin(user_id):
    """Toggle user admin status"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    admin_user = get_user_by_id(session['user_id'])
    if not admin_user or not admin_user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    user_to_update = find_one_document('users', {'id': user_id})

    if not user_to_update:
        return jsonify({'error': 'User not found'}), 404

    new_admin_status = not user_to_update.get('is_admin', False)
    update_document('users', {'id': user_id}, {'$set': {'is_admin': new_admin_status}})
    user_to_update['is_admin'] = new_admin_status

    # Log admin action
    action = 'ADMIN_GRANT_ADMIN' if user_to_update['is_admin'] else 'ADMIN_REVOKE_ADMIN'
    log_activity(admin_user['id'], action, f"{'Granted' if user_to_update['is_admin'] else 'Revoked'} admin privileges for: {user_to_update['name']}")

    return jsonify({'success': True, 'is_admin': user_to_update['is_admin']})

@app.route('/admin/api/item/<item_id>', methods=['DELETE'])
def admin_delete_item(item_id):
    """Delete item via API"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    admin_user = get_user_by_id(session['user_id'])
    if not admin_user or not admin_user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    item_to_delete = find_one_document('items', {'id': item_id})

    if not item_to_delete:
        return jsonify({'error': 'Item not found'}), 404

    # Remove item
    delete_document('items', {'id': item_id})

    # Log admin action
    log_activity(admin_user['id'], 'ADMIN_DELETE_ITEM', f"Deleted item: {item_to_delete['title']} by user {item_to_delete['user_id']}")

    return jsonify({'success': True, 'message': 'Item deleted successfully'})

@app.route('/admin/api/stats', methods=['GET'])
def admin_api_stats():
    """Get real-time admin statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = get_user_by_id(session['user_id'])
    if not user or not user.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403

    users = find_documents('users')
    items = find_documents('items')
    exchanges = find_documents('exchanges')
    activity_stats = get_activity_stats()

    stats = {
        'total_users': len(users),
        'total_items': len(items),
        'active_items': len([item for item in items if item['status'] == 'available']),
        'total_exchanges': len(exchanges),
        'completed_exchanges': len([ex for ex in exchanges if ex['status'] == 'completed']),
        'total_points': sum(user.get('points', 0) for user in users),
        'activity_stats': activity_stats
    }

    return jsonify(stats)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    try:
        # Check if database is accessible
        users = find_documents('users')
        items = find_documents('items')

        return jsonify({
            'status': 'operational',
            'database': 'connected',
            'users_count': len(users),
            'items_count': len(items),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
