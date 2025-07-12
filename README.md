**Vanquiser**
# 👗 ReWear - Sustainable Fashion Exchange Platform

A modern, comprehensive web application for exchanging fashion items sustainably. Built with Flask, featuring advanced user management, analytics, and a world-class admin dashboard.

## 🌟 Features

### Core Functionality
- **User Registration & Authentication** - Secure user accounts with session management
- **Item Upload & Management** - Upload clothing items with photos and detailed descriptions
- **Browse & Search** - Discover items by category, search terms, and filters
- **Points-Based Exchange System** - Earn and spend points for sustainable exchanges
- **User Dashboard** - Manage your items, track exchanges, and view statistics
- **Admin Panel** - Comprehensive admin interface for platform management
- **Email Notifications** - Beautiful HTML emails for all user activities

### Design & Technology
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile devices
- **Modern UI/UX** - Beautiful interface using Bootstrap 5 and Tailwind CSS
- **Interactive Elements** - Smooth animations, hover effects, and dynamic content
- **World-Class Design** - Professional gradient backgrounds, modern cards, and intuitive navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd REWEAR2
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize demo data** (optional but recommended)
   ```bash
   python init_demo_data.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 👥 Demo Accounts

After running the demo data initialization, you can use these accounts:

- **Regular User**: `demo@rewear.com` / `demo123`
- **Admin User**: `admin@rewear.com` / `admin123` ⭐ (Full Admin Access)
- **Other Users**: `sarah@example.com`, `mike@example.com`, `emma@example.com` / `password123`

## 🔧 Admin Panel Access

**How to Access Admin Features:**
1. **Login with admin credentials:** `admin@rewear.com` / `admin123`
2. **Navigate to Admin Panel:** Click your name → "Admin Panel" in navigation
3. **Direct URL:** `http://localhost:5000/admin`
4. **Detailed Guide:** See `ADMIN_ACCESS.md` for complete admin documentation

**Admin Capabilities:**
- ✅ View all users, items, and exchanges
- ✅ Monitor platform statistics in real-time
- ✅ Moderate content and manage platform settings
- ✅ Access comprehensive admin dashboard

## 📧 Email Notification System

**Comprehensive Email Features:**
- ✅ **Welcome Emails** - Beautiful HTML emails for new users
- ✅ **Login Notifications** - Email confirmation on every login
- ✅ **Upload Confirmations** - Email when items are uploaded
- ✅ **Exchange Notifications** - Emails for both parties in exchanges
- ✅ **Points Updates** - Notifications when points change
- ✅ **Professional Design** - Responsive HTML templates with branding
- ✅ **Asynchronous Sending** - Non-blocking email delivery

**Email Configuration:**
- **Gmail Integration** - Uses provided Gmail credentials
- **SMTP Settings** - Configured for Gmail SMTP
- **Error Handling** - Graceful fallback if emails fail
- **See `EMAIL_SYSTEM_GUIDE.md`** for complete documentation

## 📱 Platform Overview

### For Users
1. **Sign Up** - Create your account and get 100 starting points
2. **Upload Items** - Share your unused clothing with the community
3. **Browse & Exchange** - Find items you love and exchange using points
4. **Manage Dashboard** - Track your items, points, and exchange history

### For Admins
- **User Management** - View and manage all platform users
- **Item Moderation** - Review and moderate uploaded items
- **Exchange Monitoring** - Track all platform exchanges
- **Platform Settings** - Configure platform-wide settings

## 🎨 Design Features

### Visual Design
- **Gradient Backgrounds** - Beautiful color gradients throughout the interface
- **Modern Cards** - Clean, shadow-enhanced card layouts
- **Responsive Grid** - Perfect layout on all screen sizes
- **Professional Typography** - Poppins font family for modern appeal

### Interactive Elements
- **Smooth Animations** - Fade-in effects and hover animations
- **Dynamic Forms** - Real-time validation and feedback
- **Image Upload** - Drag-and-drop file upload with preview
- **Modal Dialogs** - Elegant confirmation and detail modals

### User Experience
- **Intuitive Navigation** - Clear menu structure and breadcrumbs
- **Search & Filter** - Powerful search with category filtering
- **Mobile-First** - Optimized for mobile devices
- **Accessibility** - Screen reader friendly and keyboard navigation

## 🛠️ Technical Stack

### Backend
- **Flask** - Python web framework
- **Werkzeug** - WSGI utilities and security
- **JSON Storage** - File-based data storage (easily replaceable with MongoDB)

### Frontend
- **Bootstrap 5** - Responsive CSS framework
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icon library
- **Vanilla JavaScript** - Interactive functionality

### Features
- **File Upload** - Secure image upload with validation
- **Session Management** - Secure user authentication
- **Form Validation** - Client and server-side validation
- **Responsive Images** - Optimized image display

## 📁 Project Structure

```
REWEAR2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── init_demo_data.py     # Demo data initialization
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── browse.html       # Browse items page
│   ├── upload.html       # Upload item page
│   ├── item_detail.html  # Item detail page
│   └── admin.html        # Admin panel
├── static/               # Static files
│   └── uploads/          # Uploaded images
├── data/                 # JSON data files (created automatically)
│   ├── users.json        # User data
│   ├── items.json        # Item data
│   └── exchanges.json    # Exchange data
```

## 🌱 Sustainability Impact

ReWear promotes sustainable fashion by:
- **Reducing Textile Waste** - Giving clothes a second life
- **Community Building** - Connecting like-minded individuals
- **Circular Economy** - Promoting reuse over disposal
- **Environmental Awareness** - Educating users about sustainable practices

## 🔧 Customization

### Adding New Features
- **Database Integration** - Replace JSON files with MongoDB or PostgreSQL
- **Payment System** - Add premium features or monetary transactions
- **Messaging System** - Enable user-to-user communication
- **Rating System** - Add user and item ratings

### Styling Customization
- **Color Schemes** - Modify CSS variables for different themes
- **Layout Changes** - Adjust Bootstrap grid and components
- **Animation Effects** - Customize JavaScript animations

## 📞 Support

For questions, suggestions, or issues:
- Check the code comments for implementation details
- Review the demo data for example usage
- Modify the platform to suit your specific needs

## 🎯 Future Enhancements

- **Mobile App** - Native iOS and Android applications
- **AI Recommendations** - Smart item suggestions
- **Social Features** - User profiles and social interactions
- **Analytics Dashboard** - Detailed platform analytics
- **Multi-language Support** - International accessibility

---

**ReWear** - Making sustainable fashion accessible to everyone! 🌍♻️👕
=======
# Vanquiser

Team Name: Vanquiser
Problem Statement:

ReWear – Community Clothing Exchange
Overview:
Develop ReWear, a web-based platform that enables users to exchange unused clothing
through direct swaps or a point-based redemption system. The goal is to promote sustainable
fashion and reduce textile waste by encouraging users to reuse wearable garments instead of
discarding them.
Features:
User Authentication
Email/password signup and login
Landing Page
Platform introduction
Calls-to-action: “Start Swapping”, “Browse Items”, “List an Item”
Featured items carousel
User Dashboard
Profile details and points balance
Uploaded items overview
Ongoing and completed swaps list
Item Detail Page
Image gallery and full item description
Uploader info
Options: “Swap Request” or “Redeem via Points”
Item availability status
Add New Item Page
Upload images
Enter title, description, category, type, size, condition, and tags
Submit to list item
Admin Role
Moderate and approve/reject item listings
Remove inappropriate or spam items
Lightweight admin panel for oversight
>>>>>>> 69bc942dc2430fa95f3e838c42f9f4583d3d37fb
