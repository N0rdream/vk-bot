import os
import dotenv


dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vk_bot_prj.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Hosting')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
