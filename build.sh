#!/usr/bin/env bash
# Build script untuk Render.com

set -o errexit  # Exit on error

echo "🚀 Starting build process..."
echo "📂 Working directory: $(pwd)"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create staticfiles directory
echo "📁 Creating staticfiles directory..."
mkdir -p staticfiles

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear --verbosity 1

# Verify static files were collected
echo "📁 Verifying static files collection..."
if [ -d "staticfiles" ] && [ "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "✅ Static files collected successfully!"
    echo "📊 Static files count: $(find staticfiles -type f | wc -l)"
else
    echo "⚠️  WARNING: Static files directory is empty!"
    echo "📂 Listing staticfiles directory:"
    ls -la staticfiles/ || echo "Directory does not exist"
fi

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "✅ Build completed successfully!"

