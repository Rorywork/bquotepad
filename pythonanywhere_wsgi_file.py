import os
import sys 

path = '/home/Rorywork/src/bquotepad'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bquotepad.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()