from .application import WhatsappProcessor


def handler(event, context):
    """Lambda handler entry point."""
    processor = WhatsappProcessor(**event)
    processor.execute()
