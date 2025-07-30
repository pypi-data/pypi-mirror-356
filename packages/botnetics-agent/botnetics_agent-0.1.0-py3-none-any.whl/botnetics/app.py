import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Global app instance
_current_app = None

def get_current_app():
    return _current_app

class BotneticsApp:
    def __init__(self, api_key, gateway_url=None):
        self.api_key = api_key
        self.gateway_url = gateway_url
        self.message_handlers = []
        self._configure_django()
        
        global _current_app
        _current_app = self
    
    def _configure_django(self):
        if not settings.configured:
            settings.configure(
                DEBUG=True,
                SECRET_KEY='botnetics-secret-key-change-in-production',
                ROOT_URLCONF='botnetics.urls',
                INSTALLED_APPS=[
                    'django.contrib.contenttypes',
                    'django.contrib.auth',
                    'corsheaders',
                    'botnetics',
                ],
                MIDDLEWARE=[
                    'corsheaders.middleware.CorsMiddleware',
                    'django.middleware.common.CommonMiddleware',
                ],
                CORS_ALLOW_ALL_ORIGINS=True,  # For development only
                USE_TZ=True,
            )
            django.setup()
    
    def on_message(self, func):
        """Decorator to register message handlers"""
        self.message_handlers.append(func)
        return func
    
    def run(self, host='0.0.0.0', port=8000):
        """Start the Django development server"""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botnetics.settings')
        execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])
