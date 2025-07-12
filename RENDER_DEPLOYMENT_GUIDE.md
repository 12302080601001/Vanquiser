# 🚀 ReWear - Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Gmail App Password** - For email functionality

## 🔧 Deployment Steps

### Step 1: Prepare Your Repository

1. **Push all files to GitHub** including:
   - `app.py` (updated with environment variables)
   - `requirements.txt` (updated with all dependencies)
   - `Procfile` (for gunicorn configuration)
   - `runtime.txt` (Python version specification)
   - `render.yaml` (Render configuration)
   - `.gitignore` (to exclude sensitive files)
   - All templates, static files, and data files

### Step 2: Create Render Web Service

1. **Login to Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Web Service"

2. **Connect GitHub Repository**
   - Select "Build and deploy from a Git repository"
   - Connect your GitHub account
   - Select your ReWear repository

3. **Configure Service Settings**
   ```
   Name: rewear-app (or your preferred name)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

### Step 3: Set Environment Variables

In the Render dashboard, add these environment variables:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=mkbharvad534@gmail.com
MAIL_PASSWORD=dwtp fmiq miyl ccvq
MAIL_DEFAULT_SENDER=mkbharvad534@gmail.com

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# Database Configuration
DATABASE_URL=mongodb+srv://mkbharvad8080:Mkb%408080@cluster0.a82h2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

## 🔧 Troubleshooting Deployment Issues

### Issue: "gunicorn: command not found"

**Solution 1: Check Build Logs**
- Go to your Render dashboard
- Click on your service
- Check the "Build Logs" tab for any installation errors

**Solution 2: Manual Build Commands**
If the automated build fails, try these manual commands in the Render shell:

```bash
# Update pip and install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Verify gunicorn installation
which gunicorn
gunicorn --version

# Test the application
python app.py
```

**Solution 3: Alternative Start Command**
If gunicorn still doesn't work, try using Python directly:

```bash
# In Render dashboard, change the start command to:
python app.py
```

**Solution 4: Check Python Version**
Ensure you're using Python 3.10.12 as specified in `runtime.txt`

### Issue: MongoDB Connection Errors

**Solution:**
1. Verify the DATABASE_URL environment variable is set correctly
2. Check MongoDB Atlas network access settings
3. Ensure the cluster is running and accessible

### Issue: Static Files Not Loading

**Solution:**
1. Ensure the `static` folder is included in your repository
2. Check that `UPLOAD_FOLDER` environment variable is set to `static/uploads`
3. Verify file permissions in the deployment environment
```

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 5-10 minutes)
3. **Check logs** for any errors
4. **Test your application** using the provided Render URL

## 📁 File Structure for Deployment

```
REWEAR2/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Procfile                   # Gunicorn configuration
├── runtime.txt                # Python version
├── render.yaml                # Render configuration
├── .gitignore                 # Git ignore rules
├── .env                       # Environment variables (local)
├── remove_duplicates.py       # Utility script
├── data/                      # JSON data files
│   ├── users.json
│   ├── items.json
│   ├── exchanges.json
│   ├── activity_logs.json
│   └── wishlist.json
├── static/                    # Static assets
│   ├── css/
│   ├── js/
│   └── uploads/              # User uploaded images
└── templates/                 # HTML templates
    ├── base.html
    ├── index.html
    ├── dashboard.html
    ├── browse.html
    ├── admin.html
    └── ...
```

## 🔒 Security Considerations

1. **Environment Variables**: All sensitive data is stored in environment variables
2. **Secret Key**: Use Render's auto-generated secret key
3. **Email Credentials**: Stored securely in environment variables
4. **File Uploads**: Limited to 16MB with secure filename handling

## 🌐 Domain Configuration

1. **Custom Domain** (Optional):
   - Go to Settings → Custom Domains
   - Add your domain
   - Configure DNS records as instructed

2. **SSL Certificate**:
   - Automatically provided by Render
   - HTTPS enabled by default

## 📊 Monitoring & Logs

1. **View Logs**:
   - Go to your service dashboard
   - Click "Logs" tab
   - Monitor real-time application logs

2. **Metrics**:
   - CPU and Memory usage
   - Request metrics
   - Error tracking

## 🔄 Continuous Deployment

- **Auto-deploy**: Enabled by default
- **Manual deploy**: Available in dashboard
- **Branch selection**: Choose main/master branch

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check requirements.txt for correct versions
   - Verify Python version in runtime.txt

2. **Email Not Working**:
   - Verify Gmail app password
   - Check environment variables

3. **File Upload Issues**:
   - Ensure upload folder exists
   - Check file size limits

4. **Database Persistence**:
   - JSON files are stored in the container
   - Consider upgrading to PostgreSQL for production

### Debug Commands:
```bash
# Check logs
render logs --service-id your-service-id

# Restart service
render restart --service-id your-service-id
```

## 📈 Performance Optimization

1. **Static Files**: Served efficiently by Render
2. **Caching**: Implement Redis for session storage
3. **Database**: Upgrade to PostgreSQL for better performance
4. **CDN**: Use Render's built-in CDN for static assets

## 🔄 Updates & Maintenance

1. **Code Updates**: Push to GitHub → Auto-deploy
2. **Dependency Updates**: Update requirements.txt
3. **Environment Variables**: Update in Render dashboard
4. **Monitoring**: Regular log checking

## 📞 Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Community Forum**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

---

## 🎉 Your ReWear App is Now Live!

After successful deployment, your sustainable fashion exchange platform will be accessible worldwide with:

- ✅ Secure HTTPS connection
- ✅ Automatic SSL certificates
- ✅ Global CDN distribution
- ✅ Continuous deployment
- ✅ Professional monitoring
- ✅ Email notifications
- ✅ Admin dashboard
- ✅ User management
- ✅ Real-time analytics

**Happy Deploying! 🚀**
