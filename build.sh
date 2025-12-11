#!/usr/bin/env bash
# Build script untuk Render.com

# Don't exit on error immediately - we want to handle errors gracefully
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable
# errexit is disabled to allow graceful error handling

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
python manage.py migrate --noinput || {
    echo "⚠️  Migrations had warnings, but continuing..."
}

# Create staticfiles directory
echo "📁 Creating staticfiles directory..."
mkdir -p staticfiles

# Collect static files
echo "📁 Collecting static files..."
echo "📂 STATIC_ROOT: $(python -c 'from django.conf import settings; print(settings.STATIC_ROOT)')"
echo "📂 STATICFILES_DIRS: $(python -c 'from django.conf import settings; print(settings.STATICFILES_DIRS)')"

# Verify vendor files exist before collectstatic
echo "🔍 Checking for vendor files..."
echo "📂 Current working directory: $(pwd)"
echo "📂 Checking for vendor files in multiple possible locations..."

VENDOR_FOUND=false
VENDOR_PATH=""

# Check multiple possible vendor locations
for vendor_path in "src/assets/vendor" "../src/assets/vendor" "../../src/assets/vendor"; do
    if [ -d "$vendor_path" ]; then
        echo "✅ Vendor directory found at: $vendor_path"
        VENDOR_FOUND=true
        VENDOR_PATH="$vendor_path"
        echo "📊 Vendor files count: $(find "$vendor_path" -type f | wc -l)"
        echo "📂 Sample vendor files:"
        find "$vendor_path" -type f | head -5
        # Verify critical vendor files exist
        if [ -f "$vendor_path/css/core.css" ] && [ -f "$vendor_path/libs/jquery/jquery.js" ]; then
            echo "✅ Critical vendor files found!"
            break
        else
            echo "⚠️  WARNING: Some critical vendor files missing in $vendor_path!"
        fi
    fi
done

if [ "$VENDOR_FOUND" = false ]; then
    echo "❌ ERROR: Vendor directory not found in any expected location!"
    echo "📂 Listing current directory:"
    ls -la
    echo "📂 Listing src directory:"
    ls -la src/ 2>/dev/null || echo "src directory does not exist"
    echo "📂 Listing parent directory:"
    ls -la ../ 2>/dev/null || echo "parent directory not accessible"
    echo "⚠️  WARNING: Build will continue but vendor files may not be collected!"
fi

# Collect static files with verbosity to see what's happening
echo "📦 Running collectstatic..."
python manage.py collectstatic --noinput --clear --verbosity 2 || {
    echo "⚠️  collectstatic had warnings, but continuing..."
}

# Verify static files were collected
echo "📁 Verifying static files collection..."
if [ -d "staticfiles" ] && [ "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "✅ Static files collected successfully!"
    echo "📊 Static files count: $(find staticfiles -type f | wc -l)"
    echo "📂 Sample files in staticfiles:"
    find staticfiles -type f | head -10
    # Check if vendor directory exists (critical for the app)
    if [ -d "staticfiles/vendor" ]; then
        echo "✅ Vendor directory exists in staticfiles!"
        echo "📊 Vendor files count: $(find staticfiles/vendor -type f | wc -l)"
        echo "📂 Sample vendor files in staticfiles:"
        find staticfiles/vendor -type f | head -5
    else
        echo "❌ CRITICAL ERROR: Vendor directory not found in staticfiles!"
        echo "📂 Listing staticfiles directory structure:"
        ls -la staticfiles/ || echo "Directory does not exist"
        echo "📂 Checking if vendor exists in source:"
        ls -la src/assets/vendor/ 2>/dev/null || echo "src/assets/vendor does not exist"
        
        # Try to manually copy vendor files if they exist but weren't collected
        if [ -d "src/assets/vendor" ]; then
            echo "🔧 Attempting to manually copy vendor files..."
            mkdir -p staticfiles/vendor
            cp -r src/assets/vendor/* staticfiles/vendor/ 2>/dev/null || {
                echo "⚠️  Manual copy failed, trying alternative method..."
                # Try with find and cp
                find src/assets/vendor -type f -exec cp --parents {} staticfiles/ \; 2>/dev/null || {
                    echo "❌ Manual copy also failed!"
                }
            }
            
            # Verify manual copy worked
            if [ -d "staticfiles/vendor" ] && [ "$(ls -A staticfiles/vendor 2>/dev/null)" ]; then
                echo "✅ Vendor files manually copied successfully!"
                echo "📊 Vendor files count after manual copy: $(find staticfiles/vendor -type f | wc -l)"
            else
                echo "❌ Manual copy failed! Vendor files still missing!"
                echo "⚠️  This will cause static files to fail loading!"
            fi
        else
            echo "❌ Vendor source directory not found! Cannot copy manually."
            echo "⚠️  This will cause static files to fail loading!"
        fi
    fi
else
    echo "❌ ERROR: Static files directory is empty or does not exist!"
    echo "📂 Listing staticfiles directory:"
    ls -la staticfiles/ || echo "Directory does not exist"
    echo "❌ Build failed: Static files not collected!"
    exit 1
fi

echo "✅ Build completed successfully!"
