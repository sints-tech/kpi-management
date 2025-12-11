#!/usr/bin/env bash
# Build script untuk Render.com

set -o errexit  # Exit on error

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
echo "📁 Creating staticfiles directory..."
mkdir -p staticfiles

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "✅ Build completed successfully!"

