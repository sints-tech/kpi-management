#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable

echo "Starting build process..."

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies (ensure all packages are installed, especially Pillow)
# Note: Render.com usually installs automatically, but we ensure it here
echo "Installing/verifying dependencies..."
pip install -r requirements.txt --quiet

# Verify critical packages installation
echo "Verifying critical packages..."
python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')" || {
    echo "❌ Error: Pillow installation failed!"
    pip install Pillow --upgrade
    python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')"
}

python -c "import django; print(f'✅ Django version: {django.__version__}')"

# Run system check first to catch issues early
echo "Running Django system check..."
python manage.py check --deploy || {
    echo "⚠️ System check found issues, but continuing..."
}

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"

