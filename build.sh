#!/usr/bin/env bash
# Build script untuk Render.com

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable

echo "🚀 Starting build process..."
echo "📂 Working directory: $(pwd)"

# Upgrade pip to latest version
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install Pillow FIRST (critical for ImageField) - explicitly install before other packages
echo "📸 Installing Pillow (required for ImageField)..."
pip install Pillow==10.4.0 --quiet || {
    echo "⚠️ Pillow installation with version failed, trying latest..."
    pip install --upgrade Pillow --quiet
}

# Verify Pillow installation immediately
echo "🔍 Verifying Pillow installation..."
python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')" || {
    echo "❌ CRITICAL: Pillow is not installed! Attempting emergency install..."
    pip install --force-reinstall Pillow --quiet
    python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')" || {
        echo "❌ FATAL: Cannot install Pillow. Please check Python version and system dependencies."
        exit 1
    }
}

# Install other dependencies from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

# Verify critical packages installation
echo "🔍 Verifying critical packages..."
python -c "import django; print(f'✅ Django version: {django.__version__}')"
python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')"

# Run system check first to catch issues early (before migrations)
echo "🔍 Running Django system check..."
python manage.py check --deploy || {
    echo "⚠️ System check found issues, but continuing..."
}

# Run migrations (Pillow must be installed before this)
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

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

echo "✅ Build completed successfully!"

