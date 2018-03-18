import os
from celery import Celery
import dotenv


dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vk_bot_prj.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Hosting')

import configurations
configurations.setup()

app = Celery('vk_bot_prj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
