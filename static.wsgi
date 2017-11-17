import sys
sys.path.insert(0, '/var/www/static')

from static import app as application

application.debug = True

sys.stdout = sys.stderr