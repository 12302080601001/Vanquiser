# Admin Access Guide - ReWear Platform

## How to Access Admin Panel

### Method 1: Using Demo Admin Account
1. **Login with Admin Credentials:**
   - Email: `admin@rewear.com`
   - Password: `admin123`

2. **Navigate to Admin Panel:**
   - After login, click on your name in the top navigation
   - Select "Admin Panel" from the dropdown menu
   - Or directly visit: `http://localhost:5000/admin`

### Method 2: Making Any User an Admin
1. **Stop the Flask application** (Ctrl+C in terminal)

2. **Edit the user data file:**
   - Open `data/users.json`
   - Find the user you want to make admin
   - Change `"is_admin": false` to `"is_admin": true`
   - Save the file

3. **Restart the application:**
   ```bash
   python app.py
   ```

4. **Login with that user** and access admin panel

### Method 3: Create New Admin User
1. **Register a new account** normally through the website
2. **Follow Method 2** to edit the JSON file
3. **Login and access admin panel**

## Admin Panel Features

### 📊 Dashboard Statistics
- **Total Users:** View all registered users
- **Total Items:** See all uploaded items
- **Active Items:** Items available for exchange
- **Total Exchanges:** All exchange transactions
- **Completed Exchanges:** Successfully completed trades
- **Total Points:** Points in circulation

### 👥 User Management
- **View All Users:** Complete user list with details
- **User Information:** Name, email, points, join date
- **Admin Status:** See which users have admin privileges
- **User Actions:** Edit and delete user accounts (coming soon)

### 🛍️ Item Management
- **View All Items:** Complete item catalog
- **Item Details:** Title, category, points, status, owner
- **Item Moderation:** Flag inappropriate content
- **Item Actions:** View, moderate, or delete items

### 🔄 Exchange Monitoring
- **Exchange History:** All platform exchanges
- **Transaction Details:** Item, users involved, points transferred
- **Exchange Status:** Track completion status
- **Data Export:** Export exchange data (coming soon)

### ⚙️ Platform Settings
- **General Settings:** Platform name, default points, file limits
- **Moderation Settings:** Auto-approval, notifications, maintenance mode
- **Configuration:** Customize platform behavior

## Admin Privileges

### What Admins Can Do:
✅ **View all platform data and statistics**  
✅ **Access user management interface**  
✅ **Monitor all item uploads and exchanges**  
✅ **Moderate content and flag inappropriate items**  
✅ **Configure platform settings**  
✅ **Export data for analysis**  
✅ **View detailed exchange history**  
✅ **Access admin-only navigation menu**  

### What Admins Cannot Do (Yet):
❌ **Delete users directly from interface** (requires JSON editing)  
❌ **Edit user details from interface** (requires JSON editing)  
❌ **Delete items directly from interface** (requires JSON editing)  
❌ **Send notifications to users** (feature planned)  
❌ **Bulk operations** (feature planned)  

## Security Notes

### Admin Account Security:
- **Change default admin password** in production
- **Limit admin access** to trusted users only
- **Monitor admin actions** through logs
- **Regular security audits** recommended

### Data Protection:
- **User data is stored in JSON files** (consider database for production)
- **No encryption** on stored passwords (uses Werkzeug hashing)
- **File-based storage** is suitable for development/demo only

## Troubleshooting Admin Access

### Problem: "Access Denied" Message
**Solution:**
1. Check if user has `"is_admin": true` in `data/users.json`
2. Restart the Flask application after JSON changes
3. Clear browser cache and login again

### Problem: Admin Panel Not Loading
**Solution:**
1. Ensure you're logged in as an admin user
2. Check Flask console for error messages
3. Verify `data/users.json` file exists and is valid JSON

### Problem: Can't See Admin Panel Link
**Solution:**
1. The admin link only appears for admin users
2. Check user's admin status in JSON file
3. Refresh the page after making changes

### Problem: JSON File Corruption
**Solution:**
1. Backup your data files regularly
2. Use a JSON validator to check file syntax
3. Re-run `python init_demo_data.py` to reset demo data

## Production Recommendations

### For Production Deployment:
1. **Use a proper database** (PostgreSQL, MongoDB)
2. **Implement role-based permissions** with more granular control
3. **Add audit logging** for all admin actions
4. **Use environment variables** for sensitive configuration
5. **Implement proper authentication** (OAuth, JWT)
6. **Add rate limiting** and security headers
7. **Use HTTPS** for all communications
8. **Regular backups** of user data

### Database Migration:
When moving to production, consider migrating from JSON files to:
- **PostgreSQL** for relational data
- **MongoDB** for document-based storage
- **Redis** for session management
- **AWS S3** for image storage

## Support

For technical support or questions about admin functionality:
1. Check the Flask console for error messages
2. Review the `app.py` file for admin route logic
3. Examine JSON data files for data integrity
4. Test with demo admin account first

---

**Remember:** This is a development/demo platform. For production use, implement proper database storage, authentication, and security measures.
