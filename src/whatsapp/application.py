import logging
import json
from datetime import datetime, timezone
from typing import Any
import urllib.request
import urllib.error

from pydoover.cloud.processor import ProcessorBase

from .app_config import WhatsappConfig

log = logging.getLogger()


class WhatsappProcessor(ProcessorBase):
    """WhatsApp processor for sending threshold-based alerts.

    This processor monitors channel messages for tag values and sends
    WhatsApp alerts when configured thresholds are violated.

    Configuration options:
    - Channel subscriptions to monitor
    - Threshold definitions with operators (>, <, >=, <=, ==, !=)
    - Custom message templates
    - Alert cooldown periods to prevent spam
    - WhatsApp Business API credentials
    - Recipient phone numbers
    """

    def setup(self):
        """Called once per invocation before processing."""
        log.info("WhatsApp processor setup complete")

        # Parse the package config into our config schema
        self.config = WhatsappConfig()
        self.config.from_dict(self.package_config)

    def process(self):
        """Process incoming messages and check for threshold violations."""
        if not self._is_enabled():
            log.info("WhatsApp alerts are disabled")
            return

        if self.message is None:
            log.info("No message to process (schedule or manual trigger)")
            self._handle_schedule_or_manual()
            return

        # Get the message data
        data = self.message.data
        log.info(f"Received message: {data}")

        # Check if data contains any monitored tags
        self._check_thresholds(data)

    def close(self):
        """Called once per invocation after processing."""
        pass

    def _is_enabled(self) -> bool:
        """Check if WhatsApp alerts are enabled."""
        return self.config.enabled.value if self.config.enabled.value is not None else True

    def _handle_schedule_or_manual(self):
        """Handle scheduled or manual invocations."""
        # Update last run timestamp
        self._set_tag("last_scheduled_run", datetime.now(timezone.utc).isoformat())

    def _check_thresholds(self, data: dict[str, Any]):
        """Check data against configured thresholds and send alerts if violated."""
        thresholds = self.config.thresholds.value
        if not thresholds:
            log.debug("No thresholds configured")
            return

        # Get alert cooldown state
        cooldown_state = self._get_tag("alert_cooldowns", {})

        for threshold_config in thresholds:
            tag_name = threshold_config.get("tag_name")
            if not tag_name:
                continue

            # Check if the tag exists in the data
            value = self._extract_value(data, tag_name)
            if value is None:
                continue

            operator = threshold_config.get("operator", ">")
            threshold_value = threshold_config.get("threshold_value", 0.0)

            # Check if threshold is violated
            if self._is_threshold_violated(value, operator, threshold_value):
                # Check cooldown
                cooldown_key = f"{tag_name}_{operator}_{threshold_value}"
                cooldown_minutes = threshold_config.get("cooldown_minutes", 15)

                if self._is_in_cooldown(cooldown_state, cooldown_key, cooldown_minutes):
                    log.info(f"Threshold alert for '{tag_name}' is in cooldown, skipping")
                    continue

                # Format and send the alert message
                message = self._format_message(
                    threshold_config.get("message_template", "Alert: {tag_name} is {value}"),
                    tag_name=tag_name,
                    value=value,
                    threshold=threshold_value,
                    operator=operator,
                    device_name=self.agent_id
                )

                self._send_whatsapp_message(message)

                # Update cooldown state
                cooldown_state[cooldown_key] = datetime.now(timezone.utc).isoformat()
                self._set_tag("alert_cooldowns", cooldown_state)

                log.info(f"Sent WhatsApp alert for threshold violation: {tag_name} {operator} {threshold_value}")

    def _extract_value(self, data: dict[str, Any], tag_name: str) -> float | None:
        """Extract a numeric value from nested data using dot notation."""
        if not isinstance(data, dict):
            return None

        # Support dot notation for nested values (e.g., "sensors.temperature")
        keys = tag_name.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        # Try to convert to float
        try:
            return float(current)
        except (TypeError, ValueError):
            return None

    def _is_threshold_violated(self, value: float, operator: str, threshold: float) -> bool:
        """Check if a value violates the threshold based on the operator."""
        operators = {
            ">": lambda v, t: v > t,
            "<": lambda v, t: v < t,
            ">=": lambda v, t: v >= t,
            "<=": lambda v, t: v <= t,
            "==": lambda v, t: v == t,
            "!=": lambda v, t: v != t,
        }

        check_func = operators.get(operator, operators[">"])
        return check_func(value, threshold)

    def _is_in_cooldown(self, cooldown_state: dict, cooldown_key: str, cooldown_minutes: int) -> bool:
        """Check if an alert is still in cooldown period."""
        if cooldown_key not in cooldown_state:
            return False

        try:
            last_alert_time = datetime.fromisoformat(cooldown_state[cooldown_key])
            elapsed = datetime.now(timezone.utc) - last_alert_time
            return elapsed.total_seconds() < cooldown_minutes * 60
        except (ValueError, TypeError):
            return False

    def _format_message(self, template: str, **kwargs) -> str:
        """Format a message template with the provided values."""
        prefix = self.config.default_message_prefix.value or ""
        try:
            message = template.format(**kwargs)
            return f"{prefix} {message}".strip()
        except KeyError as e:
            log.warning(f"Message template missing key: {e}")
            return f"{prefix} Alert: {kwargs.get('tag_name', 'Unknown')} = {kwargs.get('value', 'N/A')}"

    def _get_tag(self, tag_name: str, default: Any = None) -> Any:
        """Get a tag value from the agent's deployment config."""
        try:
            channel = self.fetch_channel_named(f"@tags/{tag_name}")
            if channel and channel.get_aggregate():
                agg = channel.get_aggregate()
                return agg.data if agg.data is not None else default
            return default
        except Exception:
            return default

    def _set_tag(self, tag_name: str, value: Any):
        """Set a tag value on the agent."""
        try:
            channel = self.fetch_channel_named(f"@tags/{tag_name}")
            if channel:
                self.api.publish_to_channel(channel.id, value)
        except Exception as e:
            log.warning(f"Failed to set tag '{tag_name}': {e}")

    def _send_whatsapp_message(self, message: str):
        """Send a WhatsApp message to all configured recipients."""
        phone_number_id = self.config.whatsapp_phone_number_id.value
        access_token = self.config.whatsapp_access_token.value
        recipients = self.config.recipient_phone_numbers.value
        api_url = self.config.whatsapp_api_url.value

        if not all([phone_number_id, access_token, recipients]):
            log.error("WhatsApp configuration incomplete - missing phone_number_id, access_token, or recipients")
            return

        # Parse comma-separated phone numbers
        phone_numbers = [p.strip() for p in recipients.split(",") if p.strip()]

        for phone_number in phone_numbers:
            self._send_to_recipient(api_url, phone_number_id, access_token, phone_number, message)

    def _send_to_recipient(self, api_url: str, phone_number_id: str, access_token: str, recipient: str, message: str):
        """Send a WhatsApp message to a single recipient."""
        url = f"{api_url}/{phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient.replace("+", "").replace(" ", "").replace("-", ""),
            "type": "text",
            "text": {
                "body": message
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(request, timeout=30) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                log.info(f"WhatsApp message sent to {recipient}: {response_data}")

                # Track sent messages
                sent_count = self._get_tag("messages_sent_count", 0)
                self._set_tag("messages_sent_count", sent_count + 1)
                self._set_tag("last_message_sent", datetime.now(timezone.utc).isoformat())

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else "No response body"
            log.error(f"Failed to send WhatsApp message to {recipient}: HTTP {e.code} - {error_body}")
        except urllib.error.URLError as e:
            log.error(f"Failed to send WhatsApp message to {recipient}: {e.reason}")
        except Exception as e:
            log.error(f"Unexpected error sending WhatsApp message to {recipient}: {e}")
