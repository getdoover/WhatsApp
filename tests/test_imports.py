"""
Basic tests for an application.

This ensures all modules are importable and that the config is valid.
"""

def test_import_app():
    from whatsapp.application import WhatsappApplication
    assert WhatsappApplication

def test_config():
    from whatsapp.app_config import WhatsappConfig

    config = WhatsappConfig()
    assert isinstance(config.to_dict(), dict)

def test_ui():
    from whatsapp.app_ui import WhatsappUI
    assert WhatsappUI

def test_state():
    from whatsapp.app_state import WhatsappState
    assert WhatsappState