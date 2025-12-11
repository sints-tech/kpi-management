import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Ensure admin user exists
user, created = User.objects.get_or_create(username='admin', defaults={
    'email': 'admin@example.com',
    'is_staff': True,
    'is_superuser': True,
    'is_active': True
})
if created:
    user.set_password('admin123')
    user.save()
    print(f"Created admin user")
else:
    print(f"Admin user already exists")

# Test pages
c = Client()
c.force_login(user)

urls = [
    ('Story', '/kpi/stories/'),
    ('Daily Feed/Reels', '/kpi/daily-feeds/'),
    ('Campaign', '/kpi/campaigns/'),
    ('Social Media Account', '/kpi/social-media-accounts/'),
    ('Dashboard', '/kpi/dashboard/'),
]

print("\n" + "="*60)
print("TESTING CRUD PAGES")
print("="*60 + "\n")

for name, url in urls:
    try:
        response = c.get(url)
        status = response.status_code
        if status == 200:
            print(f"✓ {name:30} {url:40} Status: {status} OK")
        else:
            print(f"✗ {name:30} {url:40} Status: {status} ERROR")
            content = response.content.decode('utf-8', errors='ignore')
            if content:
                # Find error message
                if 'Traceback' in content:
                    idx = content.find('Traceback')
                    error_section = content[idx:idx+3000]
                    print(f"  Error traceback (first 3000 chars):")
                    print("  " + "-"*56)
                    for line in error_section.split('\n')[:50]:
                        print(f"  {line}")
                    print("  " + "-"*56)
                elif 'Error' in content or 'Exception' in content:
                    # Try to find error message
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'Error' in line or 'Exception' in line:
                            print(f"  Error found at line {i}: {line[:200]}")
                            break
    except Exception as e:
        print(f"✗ {name:30} {url:40} EXCEPTION: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
