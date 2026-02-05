# AppGen State

## Current Phase
Phase 4 - Document

## Status
completed

## App Details
- **Name:** WhatsApp
- **Description:** WhatsApp integration for doover to allow configurable alerts, configurable messages based on configurable thresholds from tag values
- **App Type:** processor
- **Has UI:** false
- **Container Registry:** ghcr.io/getdoover
- **Target Directory:** /home/sid/whatsapp
- **GitHub Repo:** getdoover/WhatsApp
- **Repo Visibility:** public
- **GitHub URL:** https://github.com/getdoover/WhatsApp

## Completed Phases
- [x] Phase 1: Creation - 2026-02-05
- [x] Phase 2: Processor Config - 2026-02-05
- [x] Phase 3: Processor Build - 2026-02-05
- [x] Phase 4: Document - 2026-02-05

## User Decisions
- App name: WhatsApp
- Description: WhatsApp integration for doover to allow configurable alerts, configurable messages based on configurable thresholds from tag values
- GitHub repo: getdoover/WhatsApp
- App type: processor
- Has UI: false

## Phase 2 Configuration Applied
- UI removed (has_ui: false)
- Removed: src/whatsapp/app_ui.py
- Modified: src/whatsapp/application.py (removed UI imports, WhatsappUI class, ui_manager calls, and UI callbacks)
- Removed: Dockerfile (processors deploy as zip packages, not containers)
- Kept: simulators/sample/Dockerfile (needed for local development)

## Phase 3 Build Completed
- Created: src/whatsapp/__init__.py - Lambda handler entry point
- Created: src/whatsapp/application.py - WhatsappProcessor class with process() method
- Created: src/whatsapp/app_config.py - Configuration schema with thresholds, WhatsApp API settings
- Updated: doover_config.json - Changed type to "PRO", added handler and lambda_config
- Created: build.sh - Build script for packaging processor
- Updated: .gitignore - Added build outputs (packages_export/, package.zip, requirements.txt)
- Removed: simulators/ directory (not needed for processors)
- Removed: src/whatsapp/app_state.py (not needed for processors)
- Removed: transitions dependency from pyproject.toml
- Verified: uv sync and import check passed

## Processor Functionality
The WhatsApp processor:
- Receives channel messages via the Doover platform
- Checks incoming data against configured thresholds
- Supports comparison operators: >, <, >=, <=, ==, !=
- Supports dot notation for nested tag values (e.g., "sensors.temperature")
- Sends WhatsApp messages via WhatsApp Business API when thresholds are violated
- Implements cooldown periods to prevent alert spam
- Supports custom message templates with variables
- Tracks alert state using Doover tags

## Configuration Options
- WhatsApp API URL (default: Facebook Graph API v18.0)
- WhatsApp Phone Number ID (required)
- WhatsApp Access Token (required)
- Recipient Phone Numbers (comma-separated, required)
- Thresholds (array of threshold configurations)
  - Tag Name
  - Operator
  - Threshold Value
  - Message Template
  - Cooldown Minutes
- Enabled (default: true)
- Default Message Prefix (default: "[Doover Alert]")

## Phase 4 Documentation Generated
- Created: README.md with comprehensive documentation
- Sections: Overview, Features, Getting Started, Configuration, Tags, How It Works, Integrations, Need Help, Version History, License
- Configuration items documented: 7 main settings + 5 threshold settings
- Tags documented: 4 status tags
- Icon URL: https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg
- GitHub URL: https://github.com/getdoover/WhatsApp

## Next Action
Documentation complete. Ready for deployment testing or further customization.
