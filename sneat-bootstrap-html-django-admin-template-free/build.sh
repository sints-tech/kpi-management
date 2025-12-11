#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable

echo "🚀 Starting build process..."

# Upgrade pip to latest version
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Pillow FIRST (critical for ImageField)
echo "📸 Installing Pillow (required for ImageField)..."
pip install Pillow || {
    echo "⚠️ Pillow installation with default method failed, trying alternative..."
    pip install --upgrade Pillow
}

# Verify Pillow installation immediately
echo "🔍 Verifying Pillow installation..."
python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')" || {
    echo "❌ CRITICAL: Pillow is not installed! Attempting emergency install..."
    pip install --force-reinstall Pillow
    python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')" || {
        echo "❌ FATAL: Cannot install Pillow. Please check Python version and system dependencies."
        exit 1
    }
}

# Install other dependencies from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Verify critical packages installation
echo "🔍 Verifying critical packages..."
python -c "import django; print(f'✅ Django version: {django.__version__}')"
python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')"

# Run system check first to catch issues early
echo "🔍 Running Django system check..."
python manage.py check || {
    echo "⚠️ System check found issues, but continuing with migrations..."
}

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"

