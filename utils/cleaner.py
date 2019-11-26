## @Author  Phillip Park
## @Details 파일들을 정리하고 간단한 처리

import os, glob
from onspace.settings import INSTALLED_APPS


class Cleaner(object):
    def __init__(self, start_path):
        self.start_path = start_path
        print(self.start_path)
        self.apps = [app for app in INSTALLED_APPS if 'django' not in app and 'rest_framework' not in app]

    def clean_migrations(self):
        for app in self.apps:
            if os.path.exists(self.start_path + '/' + app + '/migrations/'):
                os.chdir(self.start_path + '/' + app + '/migrations/')
                print(os.getcwd())
                mig_f = glob.glob('0*')
                for f in mig_f:
                    print(f + ' deleted')
                    os.remove(f)
            else:
                print("지정된 경로가 존재하지 않습니다.")
                continue

        for app in self.apps:
            if os.path.exists(self.start_path + '/' + app + '/__pycache__/'):
                os.chdir(self.start_path + '/' + app + '/__pycache__/')
                print(os.getcwd())
                pycache_f = glob.glob('0*')
                for f in pycache_f:
                    print(f + ' deleted')
                    os.remove(f)
            else:
                print("지정된 경로가 존재하지 않습니다.")
                continue
