# WhatsApp

<img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="App Icon" style="max-width: 100px;">

**WhatsApp integration for Doover to send configurable alerts based on threshold violations from tag values.**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/getdoover/WhatsApp)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/getdoover/WhatsApp/blob/main/LICENSE)

[Getting Started](#getting-started) | [Configuration](#configuration) | [Developer](https://github.com/getdoover/WhatsApp/blob/main/DEVELOPMENT.md) | [Need Help?](#need-help)

<br/>

## Overview

The WhatsApp processor enables automated alerting through WhatsApp Business API when monitored data values exceed configured thresholds. This integration bridges your Doover IoT devices and sensors with instant WhatsApp notifications, ensuring critical alerts reach your team immediately on their mobile devices.

Whether you're monitoring temperature sensors, water levels, battery voltage, or any other measurable metric, this processor can evaluate incoming data against customizable thresholds and send formatted alert messages to multiple recipients. The processor supports flexible threshold configurations with various comparison operators, making it suitable for both high-limit and low-limit monitoring scenarios.

Built-in cooldown periods prevent alert fatigue by ensuring the same threshold violation doesn't trigger repeated messages within a configurable timeframe. Custom message templates allow you to include relevant context like the tag name, current value, threshold, and device name in your alerts.

### Features

- Real-time threshold monitoring with configurable comparison operators (>, <, >=, <=, ==, !=)
- Support for nested tag values using dot notation (e.g., "sensors.temperature")
- Multiple recipient support with comma-separated phone numbers
- Customizable message templates with variable substitution
- Alert cooldown periods to prevent notification spam
- Configurable message prefix for consistent alert formatting
- WhatsApp Business API integration via Facebook Graph API

<br/>

## Getting Started

### Prerequisites

1. **WhatsApp Business Account** - You need a Meta Business account with WhatsApp Business API access
2. **WhatsApp Phone Number ID** - The ID of your registered WhatsApp Business phone number
3. **Access Token** - A valid access token for the WhatsApp Business API
4. **Recipient Phone Numbers** - Phone numbers of people who should receive alerts (with country codes)

### Installation

1. Add the WhatsApp processor to your Doover deployment through the Doover platform
2. Configure the processor with your WhatsApp Business API credentials
3. Set up channel subscriptions to receive data from your devices
4. Define thresholds for the tags you want to monitor

### Quick Start

1. Enter your WhatsApp Phone Number ID and Access Token in the configuration
2. Add recipient phone numbers (comma-separated with country codes, e.g., +1234567890)
3. Create at least one threshold configuration:
   - Set the tag name to monitor
   - Choose an operator (e.g., ">" for greater than)
   - Set the threshold value
4. Enable the processor and deploy

<br/>

## Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| **WhatsApp API URL** | WhatsApp Business API endpoint | `https://graph.facebook.com/v18.0` |
| **WhatsApp Phone Number ID** | Your WhatsApp Business phone number ID | *Required* |
| **WhatsApp Access Token** | Access token for WhatsApp Business API | *Required* |
| **Recipient Phone Numbers** | Comma-separated list of phone numbers to receive alerts (with country code, e.g., +1234567890) | *Required* |
| **Thresholds** | List of threshold configurations that trigger alerts | *Required* |
| **Enabled** | Enable or disable WhatsApp alerts | `true` |
| **Default Message Prefix** | Prefix added to all alert messages | `[Doover Alert]` |

### Threshold Configuration

Each threshold in the Thresholds array has the following options:

| Setting | Description | Default |
|---------|-------------|---------|
| **Tag Name** | Name of the tag to monitor for threshold violations (supports dot notation) | *Required* |
| **Operator** | Comparison operator: >, <, >=, <=, ==, != | `>` |
| **Threshold Value** | The threshold value to compare against | `0.0` |
| **Message Template** | Message template with variables: {tag_name}, {value}, {threshold}, {operator}, {device_name} | `Alert: {tag_name} is {value} (threshold: {operator} {threshold})` |
| **Cooldown Minutes** | Minimum time between repeated alerts for the same threshold | `15` |

### Example Configuration

```json
{
  "whatsapp_api_url": "https://graph.facebook.com/v18.0",
  "whatsapp_phone_number_id": "123456789012345",
  "whatsapp_access_token": "your_access_token_here",
  "recipient_phone_numbers": "+1234567890, +0987654321",
  "thresholds": [
    {
      "tag_name": "temperature",
      "operator": ">",
      "threshold_value": 35.0,
      "message_template": "High temperature alert: {tag_name} is {value}C on {device_name}",
      "cooldown_minutes": 30
    },
    {
      "tag_name": "battery.voltage",
      "operator": "<",
      "threshold_value": 11.5,
      "message_template": "Low battery warning: {value}V on {device_name}",
      "cooldown_minutes": 60
    }
  ],
  "enabled": true,
  "default_message_prefix": "[Doover Alert]"
}
```

<br/>

## Tags

This processor exposes the following status tags:

| Tag | Description |
|-----|-------------|
| **alert_cooldowns** | Tracks the last alert time for each threshold to enforce cooldown periods |
| **messages_sent_count** | Total count of WhatsApp messages successfully sent |
| **last_message_sent** | ISO timestamp of the most recent message sent |
| **last_scheduled_run** | ISO timestamp of the last scheduled or manual invocation |

<br/>

## How It Works

1. **The processor receives channel messages** containing data from your Doover devices and sensors through configured channel subscriptions.

2. **Incoming data is evaluated against configured thresholds** by extracting the specified tag values (supporting dot notation for nested data like "sensors.temperature").

3. **When a threshold is violated**, the processor checks if the alert is in a cooldown period to prevent duplicate notifications.

4. **If not in cooldown, a WhatsApp message is formatted** using the configured message template with variable substitution for tag name, value, threshold, operator, and device name.

5. **The message is sent via WhatsApp Business API** to all configured recipient phone numbers, with the configured message prefix prepended.

6. **Cooldown state and message counts are updated** in Doover tags to track alert history and enforce cooldown periods for subsequent violations.

<br/>

## Integrations

This processor works with:

- **WhatsApp Business API** - Meta's official API for business messaging via the Facebook Graph API
- **Doover Platform** - Receives data from any Doover-connected device or sensor
- **Channel Subscriptions** - Monitors data published to subscribed channels for threshold violations

<br/>

## Need Help?

- Email: support@doover.com
- [Doover Documentation](https://docs.doover.com)
- [App Developer Documentation](https://github.com/getdoover/WhatsApp/blob/main/DEVELOPMENT.md)

<br/>

## Version History

### v0.1.0 (Current)
- Initial release
- Threshold-based alerting with configurable comparison operators
- Support for nested tag values using dot notation
- WhatsApp Business API integration
- Multi-recipient support
- Alert cooldown periods to prevent spam
- Custom message templates with variable substitution

<br/>

## License

This app is licensed under the [Apache License 2.0](https://github.com/getdoover/WhatsApp/blob/main/LICENSE).
