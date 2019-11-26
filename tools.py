import os, sys, glob

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onspace.settings")

import django

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

### scripts ###
from utils.cleaner import Cleaner
from utils.datasend import *

from onspace.settings import INSTALLED_APPS, BASE_DIR

proj_path = BASE_DIR
sys.path.append(proj_path)
os.chdir(proj_path)
start_path = os.getcwd()

if sys.argv[1] == 'cleanmigrations':
    c = Cleaner(start_path)
    c.clean_migrations()
    db = start_path + '/db.sqlite3'
    print(db)
    if os.path.exists(db):
        os.remove(db)
        print('Removed database')

elif sys.argv[1] == 'datasend':
    # dart_send()
    # resuce_send()
    print('information complete')
    # invest_news_send()
    # portfolio_send()
    # LP_company_send()
    # prof_send()
    # main_company_send()
    # print('news complete')
    # print('datasend to database')
