"""
WSGI config for iotserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/root/miniconda3/lib/python3.7/site-packages')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotserver.settings')

application = get_wsgi_application()
