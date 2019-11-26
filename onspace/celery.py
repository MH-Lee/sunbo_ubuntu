from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onspace.settings')
app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# REFERENCE: https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
# Celerybeat 태스크 추가/정의
from celery.schedules import crontab

app.conf.beat_schedule = {
    # 'dart_update': {
    #     'task': 'dart-send',
    #     'schedule': crontab(minute='08', hour='12', day_of_week='tue'),
    #     'args': (),
    # },
    # 'rescue_update': {
    #     'task': 'rescue-send',
    #     'schedule': crontab(minute='11', hour='12', day_of_week='tue'),
    #     'args': (),
    # },

}

# 'dfb_update_check': {
#     'task': 'dealflowbox.tasks.dealflowbox_update',
#     'schedule': crontab(minute='45', hour='1', day_of_week='mon'),
#     'args': (),
# },
# 'news_update': {
#     'task': 'news.tasks.news_datasend',
#     'schedule': crontab(minute='18', hour='22', day_of_week='mon'),
#     'args': (),
# },
# 'prof_update': {
#     'task': 'news.tasks.professor_data_send',
#     'schedule': crontab(minute='23', hour='22', day_of_week='mon'),
#     'args': (),
# },