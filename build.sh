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
echo "📂 STATIC_ROOT: $(python -c 'from django.conf import settings; print(settings.STATIC_ROOT)')"
echo "📂 STATICFILES_DIRS: $(python -c 'from django.conf import settings; print(settings.STATICFILES_DIRS)')"

# Check if vendor directory exists before collectstatic
echo "📂 Checking vendor directory in source..."
if [ -d "src/assets/vendor" ]; then
    echo "✅ Vendor directory found in src/assets/vendor"
    echo "📊 Vendor files count: $(find src/assets/vendor -type f | wc -l)"
else
    echo "⚠️  WARNING: Vendor directory not found in src/assets/vendor"
fi

# Collect static files with verbosity to see what's happening
echo "📁 Running collectstatic..."
python manage.py collectstatic --noinput --clear --verbosity 2 || {
    echo "⚠️  WARNING: collectstatic had issues, but continuing..."
}

# Manually ensure vendor files are copied if they exist in source but not in staticfiles
if [ -d "src/assets/vendor" ] && [ ! -d "staticfiles/vendor" ]; then
    echo "📁 Vendor files not collected by collectstatic, copying manually..."
    mkdir -p staticfiles/vendor
    cp -r src/assets/vendor/* staticfiles/vendor/ 2>/dev/null || {
        echo "⚠️  WARNING: Failed to copy vendor files manually"
    }
    echo "✅ Vendor files copied manually"
fi

# Verify static files were collected
echo "📁 Verifying static files collection..."
if [ -d "staticfiles" ] && [ "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "✅ Static files collected successfully!"
    echo "📊 Static files count: $(find staticfiles -type f | wc -l)"
    echo "📂 Sample files in staticfiles:"
    find staticfiles -type f | head -10
    echo "📂 All directories in staticfiles:"
    find staticfiles -type d | head -20
    # Check if vendor directory exists (critical for the app)
    if [ -d "staticfiles/vendor" ]; then
        echo "✅ Vendor directory exists!"
        echo "📊 Vendor files count: $(find staticfiles/vendor -type f | wc -l)"
        echo "📂 Sample vendor files:"
        find staticfiles/vendor -type f | head -10
    else
        echo "⚠️  WARNING: Vendor directory not found in staticfiles!"
        echo "📂 Checking if vendor exists in source:"
        if [ -d "src/assets/vendor" ]; then
            echo "✅ Vendor directory exists in src/assets/vendor"
            echo "📊 Vendor files in source: $(find src/assets/vendor -type f | wc -l)"
            echo "📂 Sample vendor files in source:"
            find src/assets/vendor -type f | head -10
        else
            echo "❌ Vendor directory not found in src/assets/vendor either!"
        fi
        echo "⚠️  Continuing build despite missing vendor files (will use USE_FINDERS fallback)"
    fi
else
    echo "❌ ERROR: Static files directory is empty or does not exist!"
    echo "📂 Listing staticfiles directory:"
    ls -la staticfiles/ || echo "Directory does not exist"
    echo "❌ Build failed: Static files not collected!"
    exit 1
fi

echo "✅ Build completed successfully!"
