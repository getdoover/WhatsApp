from pathlib import Path
from typing import Any

from pydoover import config


def create_threshold_object():
    """Create a threshold configuration Object element."""
    threshold = config.Object(
        "Threshold",
        description="Configuration for a single threshold alert"
    )
    threshold.add_elements(
        config.String(
            "Tag Name",
            description="Name of the tag to monitor for threshold violations"
        ),
        config.String(
            "Operator",
            default=">",
            description="Comparison operator: >, <, >=, <=, ==, !="
        ),
        config.Number(
            "Threshold Value",
            default=0.0,
            description="The threshold value to compare against"
        ),
        config.String(
            "Message Template",
            default="Alert: {tag_name} is {value} (threshold: {operator} {threshold})",
            description="Message template. Variables: {tag_name}, {value}, {threshold}, {operator}, {device_name}"
        ),
        config.Integer(
            "Cooldown minutes",
            default=15,
            description="Minimum time between repeated alerts for the same threshold"
        ),
    )
    return threshold


class WhatsappConfig(config.Schema):
    """Configuration for the WhatsApp processor.

    This processor monitors channel messages for tag values and sends
    WhatsApp alerts when configured thresholds are violated.
    """

    def __init__(self):
        # WhatsApp API configuration
        self.whatsapp_api_url = config.String(
            "WhatsApp API URL",
            default="https://graph.facebook.com/v18.0",
            description="WhatsApp Business API endpoint"
        )
        self.whatsapp_phone_number_id = config.String(
            "WhatsApp Phone Number ID",
            description="Your WhatsApp Business phone number ID"
        )
        self.whatsapp_access_token = config.String(
            "WhatsApp Access Token",
            description="Access token for WhatsApp Business API"
        )

        # Recipient configuration
        self.recipient_phone_numbers = config.String(
            "Recipient Phone Numbers",
            description="Comma-separated list of phone numbers to receive alerts (with country code, e.g., +1234567890)"
        )

        # Threshold configurations
        self.thresholds = config.Array(
            "Thresholds",
            element=create_threshold_object(),
            description="List of threshold configurations that trigger alerts"
        )

        # General settings
        self.enabled = config.Boolean(
            "Enabled",
            default=True,
            description="Enable or disable WhatsApp alerts"
        )
        self.default_message_prefix = config.String(
            "Default Message Prefix",
            default="[Doover Alert]",
            description="Prefix added to all alert messages"
        )

    def from_dict(self, data: dict[str, Any]):
        """Load configuration from a dictionary (package_config)."""
        if not data:
            return

        if "whatsapp_api_url" in data:
            self.whatsapp_api_url._value = data["whatsapp_api_url"]
        if "whatsapp_phone_number_id" in data:
            self.whatsapp_phone_number_id._value = data["whatsapp_phone_number_id"]
        if "whatsapp_access_token" in data:
            self.whatsapp_access_token._value = data["whatsapp_access_token"]
        if "recipient_phone_numbers" in data:
            self.recipient_phone_numbers._value = data["recipient_phone_numbers"]
        if "thresholds" in data:
            self.thresholds._value = data["thresholds"]
        if "enabled" in data:
            self.enabled._value = data["enabled"]
        if "default_message_prefix" in data:
            self.default_message_prefix._value = data["default_message_prefix"]


def export():
    """Export the config schema to doover_config.json."""
    WhatsappConfig().export(
        Path(__file__).parents[2] / "doover_config.json",
        "whatsapp"
    )


if __name__ == "__main__":
    export()
