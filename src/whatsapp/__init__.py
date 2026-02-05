from pydoover.docker import run_app

from .application import WhatsappApplication
from .app_config import WhatsappConfig

def main():
    """
    Run the application.
    """
    run_app(WhatsappApplication(config=WhatsappConfig()))
