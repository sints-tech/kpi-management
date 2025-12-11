"""
WSGI config for web_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Configure logging to ensure it works in production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("=" * 60)
logger.info("WSGI APPLICATION STARTING")
logger.info("=" * 60)

application = get_wsgi_application()

# Log URL patterns after application is loaded
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    logger.info("=" * 60)
    logger.info("URL PATTERNS REGISTRATION")
    logger.info("=" * 60)
    logger.info(f"Total URL patterns: {len(resolver.url_patterns)}")
    for i, pattern in enumerate(resolver.url_patterns):
        logger.info(f"Pattern {i+1}: {pattern}")
    logger.info("=" * 60)
except Exception as e:
    logger.error(f"Error logging URL patterns: {e}", exc_info=True)
