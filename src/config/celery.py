from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную DJANGO_SETTINGS_MODULE в settings вашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Загрузите настройки из файла Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживайте и регистрируйте задачи приложения Django.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
