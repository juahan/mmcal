"""Constants for the Magic Mirror Calendar integration."""
from typing import Final

DOMAIN: Final = "magic_mirror_calendar"
CONF_CALENDAR_NAME = "calendar_name"
CONF_MAX_EVENTS = "max_events"
DEFAULT_MAX_EVENTS = 20

STARTUP_MESSAGE: Final = f"""
-------------------------------------------------------------------
{DOMAIN}
This is a custom integration for Home Assistant
-------------------------------------------------------------------
"""
