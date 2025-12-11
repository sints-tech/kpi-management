# -*- encoding: utf-8 -*-
import os

# Use PORT environment variable from Render.com, default to 5005 for local development
port = os.environ.get('PORT', '5005')
bind = f'0.0.0.0:{port}'
workers = int(os.environ.get('WEB_CONCURRENCY', 1))
accesslog = '-'
loglevel = os.environ.get('LOG_LEVEL', 'info')
capture_output = True
enable_stdio_inheritance = True
timeout = 120  # Increase timeout for Render.com
