#!/bin/bash

echo "🚀 Starting ReWear build process..."

# Update pip and install build tools
echo "📦 Updating pip and installing build tools..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Verify gunicorn installation
echo "🔍 Verifying gunicorn installation..."
which gunicorn
gunicorn --version

# Run startup script
echo "🏁 Running startup script..."
python startup.py

echo "✅ Build completed successfully!"
